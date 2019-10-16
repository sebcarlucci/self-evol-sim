# animals.py
import random
from math import sqrt

food_to_survive = 1
dist_thresh = 2
range_of_sight = 7
speed = 2

class Entity():
	def __init__(self, pos):
		self.pos = pos

	def can_reproduce(self, **kwargs):
		raise NotImplementedError()
	def can_survive(self, **kwargs):
		raise NotImplementedError()
	def reproduce(self):
		raise NotImplementedError()
	def get_pos(self):
		return self.pos

animal_limit = 100
class Animal(Entity):

	def __init__(self, posX, posY):
		self.food = 0
		self.target = None
		super().__init__((posX, posY))


	def __str__(self):
		return 'Animal: {pos} @{mem:x}'.format(pos=self.pos, mem=id(self))


	def __repr__(self):
		return 'Animal: {pos} @{mem:x}'.format(pos=self.pos, mem=id(self))


	def can_survive(self, **kwargs):
		return self.food >= food_to_survive


	def can_reproduce(self, **kwargs):
		return self.food >= food_to_survive + 1


	def seek_food(self, foods):
		if not foods or self.can_reproduce():
			self.target = None
			return

		def dist2(e1, e2):
			e1x, e1y = e1.pos
			e2x, e2y = e2.pos
			return (e1x-e1x)**2 + (e1y-e2y)**2

		food_to_eat = foods.pop()
		min_dist = dist2(self, food_to_eat)
		foods.add(food_to_eat)

		for f in foods:
			curr_dist = dist2(self, f)

			if min_dist > curr_dist:
				min_dist = curr_dist
				food_to_eat = f

		self.target = food_to_eat if min_dist <= range_of_sight else None


	def eat(self, foods):
		if self.target is None:
			return None

		food_eaten = None
		x,y = self.pos
		target_x, target_y = self.target.pos

		if (target_x - x)**2 + (target_y - y)**2 < dist_thresh**2:
			food_eaten = self.target
			self.food += 1
			self.target = None
		return food_eaten


	def reproduce(self):
		x,y = self.pos
		return Animal(x + random.uniform(-3,3), y + random.uniform(-3,3))


	def move(self, n, m):
		x,y = self.pos
		# If the animal has not found a target yet, wander randomly
		if self.target is None:
			flag = random.randint(0,1)
			delta = random.uniform(-speed,speed)
			
			if flag is 1:
				x += delta
			else:
				y += delta
		else:
			target_x, target_y = self.target.pos
			delta_x, delta_y = target_x - x, target_y - y
			dist = sqrt(delta_x**2 + delta_y**2)

			if (dist_thresh > dist and dist > 0) or dist < 0.01:
				return
			try:
				speed_x, speed_y = speed * delta_x / dist, speed * delta_y / dist
			except:
				print(dist)
				
			x += speed_x
			y += speed_y

		self.pos = (x,y)

food_limit = 50
class Food(Entity):

	def __init__(self, posX, posY):
		super().__init__((posX, posY))

	def __repr__(self):
		return 'Food: {pos} @{mem:x}'.format(pos=self.pos, mem=id(self))

	def get_roots(self):
		x,y = self.pos
		return [
			(x+1,y),
			(x-1, y),
			(x,y+1),
			(x,y-1),
			(x+1,y+1),
			(x+1,y-1),
			(x-1,y+1),
			(x-1,y-1)
		]

	def can_reproduce(self, **kwargs):
		if "neighbours" not in kwargs:
			raise IllegalArgumentException()
		neighbours = kwargs["neighbours"]

		if len(neighbours) >= food_limit:
			return False

		roots = self.get_roots()
		cnt = len(roots)
		for neighbour in neighbours:
			if neighbour.pos in roots:
				cnt -= 1
		if cnt >= 0.8 * len(roots):
			return True
		return False

	def can_survive(self, **kwargs):
		if "neighbours" not in kwargs:
			raise IllegalArgumentException()
		neighbours = kwargs["neighbours"]

		roots = self.get_roots()
		cnt = len(roots)
		for neighbour in neighbours:
			if neighbour.pos in roots:
				cnt -= 1

		if cnt > 3:
			return True
		return False
	
	def reproduce(self):
		x,y = self.pos
		return Food(x + random.randint(-3,3), y + random.randint(-3,3))