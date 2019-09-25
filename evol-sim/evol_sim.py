# evol_sim.py
import random
import math

class EvolSim:
	def __init__(self, animal_num, food_num, world_dim):
		self.animals =  
		self.food_pos = food_pos
		self.food_num = food_pos.length()
		self.world_x, self.world_y = world_dim["x"], world_dim["y"]
		self.day_len = 20
		self.time = 0
	
	def run(self, num_iter=1): 
		for i in range(0,num_iter):
			self.update_animal_pos()
			self.consume_food()
			self.time += 1
			if(self.time == self.day_len):
				self.generate()

	# 0.0.0 move animals in a random direction (4-way) with constant step
	def update_animal_pos(self):
		for a in self.animal_pos:
			flag = random.randint(0,2)
			pos = random.randint(0,1)
			if(flag is 1):
				a["x"] += 1 if pos is 1 else -1
			else:
				a["y"] += 1 if pos is 1 else -1

			x,y = world_dim.values()
			print(x,y)

	# 0.0.0 consume food on a first come first serve basis
	def consume_food(self):
		for a in self.animal_pos:
			a_pos = dict((k, a[k]) for k in ['x', 'y'] 
                                        if k in a)

			if a_pos in self.food_pos:
				a["food"] += 1
				self.food_pos.remove(a_pos)

	def generate(self):
		self.generate_food()
		self.generate_animal()

	# 0.0.0 amount of food is replenished to the same contstant amount
	def generate_food(self):
		new_food_pos = random.sample(range(0,self.world_x * self.world_y),self.food_num)
		self.food_pos = map(lambda x: dict("x") ,new_food_pos)

	def generate_animals(self, num):
		new_animal_pos = random.sample(range(0,self.world_x * self.world_y), num)
		self.animals = map(lambda n: Animal(math.floor(n/self.world_y), n % self.world_y), new_animal_pos)
		print(self.animals)

