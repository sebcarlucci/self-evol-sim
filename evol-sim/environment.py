# environment.py
import random
from animals import Animal, Food
from threading import Lock

class Chunk():

	def __init__(self, size, num, world_dim):
		self.num = num
		self.pos = int(num/world_dim[1]), num%world_dim[1]
		self.size = size
		self.animals = set()
		self.foods = set()
		self.thread_lock = Lock()


	def __repr__(self):
		return "Chunk num: {num}".format(num=self.num)


	def generate_animal(self, animal=None):
		if animal is None:
			a_pos = random.randint(0,self.size*self.size)
			a_x, a_y = int(a_pos/self.size), a_pos%self.size
			animal = Animal(a_x,a_y)
		self.animals.add(animal)


	def generate_food(self, food=None):
		if food is None:
			f_pos = random.randint(0,self.size*self.size)
			f_x, f_y = int(f_pos/self.size), f_pos%self.size
			food = Food(f_x,f_y)
		self.foods.add(food)

	# Returns true if entity is out of bound and registers the event on the update list
	# else returns false
	def handle_out_of_bound_entity(self, entity, chunks, update_list, from_chunk):
		new_pos_x, new_pos_y = entity.pos
		to_chunk_x = self.pos[0] - 1 if new_pos_x < 0 else self.pos[0] + 1 if new_pos_x >= self.size else self.pos[0]
		to_chunk_y = self.pos[1] - 1 if new_pos_y < 0 else self.pos[1] + 1 if new_pos_y >= self.size else self.pos[1]

		if to_chunk_x is not self.pos[0] or to_chunk_y is not self.pos[1]:
			entity.pos = new_pos_x%self.size, new_pos_y%self.size
			chunks_n, chunks_m = len(chunks),len(chunks[0])
			to_chunk = chunks[to_chunk_x%chunks_n][to_chunk_y%chunks_m]
			update_list.append((from_chunk, to_chunk, entity))
			return True

		return False


	def regenerate_entities(self, entities, chunks, update_list):
		new_entities = set()
		dead_entities = set()
		for e in entities:
			if e.can_reproduce(neighbours=entities):
				new_entity = e.reproduce()

				# new_entity does not belong to any chunk yet
				if not self.handle_out_of_bound_entity(new_entity, chunks, update_list, from_chunk=None):
					new_entities.add(new_entity)

			elif not e.can_survive(neighbours=entities):
				dead_entities.add(e)

			e.food = 0

		entities |= new_entities
		entities -= dead_entities


	def regenerate(self, chunks, update_list):
		self.thread_lock.acquire(True)
		self.regenerate_entities(self.foods, chunks, update_list)
		self.regenerate_entities(self.animals, chunks, update_list)
		self.thread_lock.release()
		return len(self.animals), len(self.foods)


	def update(self, chunks, update_list):
		chunks_n = len(chunks)
		chunks_m = len(chunks[0])
		chunk_x, chunk_y = self.pos
		status = {
			'eaten_foods': []
		}
		for animal in self.animals:
			animal.seek_food(self.foods)
			animal.move(self.size, self.size)
			changed_chunk = self.handle_out_of_bound_entity(animal, chunks, update_list, from_chunk=self)
			# print(changed_chunk)
			if changed_chunk and (animal.target is not None):
				print("Warning: Animal out of chunk still has target in old chunk")
			
			food_eaten = animal.eat(self.foods)

			if food_eaten is not None:
				self.thread_lock.acquire(True)
				self.foods.remove(food_eaten)
				self.thread_lock.release()
				status["eaten_foods"].append(food_eaten)

		return status


class Environment():

	def __init__(self, n, m, chunk_size=1):
		self.chunks = [[Chunk(chunk_size, i + j * m, (n,m)) for i in range(0,m)] for j in range(0,n)]
		self.n = n
		self.m = m
		self.chunk_size = chunk_size
		self.update_list = []


	def generate(self, num_animal, num_food):
		self.generate_foods(num_food)
		self.generate_animals(num_animal)


	def generate_foods(self, num):
		new_food_pos = [random.choice(range(self.n * self.m))for _ in range(num)]

		for n in new_food_pos:
			x,y = int(n/self.m), n%self.m
			chunk = self.chunks[x][y]
			chunk.generate_food()


	def generate_animals(self, num):
		new_animal_pos = [random.choice(range(self.n * self.m)) for _ in range(num)]

		for n in new_animal_pos:
			x,y = int(n/self.m), n%self.m
			chunk = self.chunks[x][y]
			chunk.generate_animal()


	def apply_update_list(self):
		for update_instr in self.update_list:
			from_chunk, to_chunk, ref = update_instr
			if from_chunk is not None:
				from_chunk.thread_lock.acquire(True)
			if to_chunk is not None:
				to_chunk.thread_lock.acquire(True)

			if type(ref) is Animal:
				if from_chunk is not None:
					from_chunk.animals.remove(ref)
				if to_chunk is not None:
					to_chunk.animals.add(ref)
			elif type(ref) is Food:
				if from_chunk is not None:
					from_chunk.foods.remove(ref)
				if to_chunk is not None:
					to_chunk.foods.add(ref)
			else:
				raise TypeNotFound()

			if from_chunk is not None:
				from_chunk.thread_lock.release()
			if to_chunk is not None:
				to_chunk.thread_lock.release()


	def clear_update_list(self):
		self.update_list = []


	def regenerate(self):
		surv_animals = 0
		surv_foods = 0

		for chunk_row in self.chunks:
			for chunk in chunk_row:
				regen_state = chunk.regenerate(self.chunks, self.update_list)
				surv_animals += regen_state[0]
				surv_foods += regen_state[1]

		self.apply_update_list()
		self.clear_update_list()
		return surv_animals, surv_foods


	def update(self):
		eaten_foods = []

		for chunk_row in self.chunks:
			for chunk in chunk_row:
				chunk_status = chunk.update(self.chunks, self.update_list)
				eaten_foods.extend(chunk_status['eaten_foods'])

		self.apply_update_list()
		self.clear_update_list()
		return eaten_foods