# evol_sim.py
import random
import math
from animals import Animal
import ui_engine_api as ui_api

# - Day Engine -> night and day logic
# - Physics Engine
#    -> animals
#    -> phyisical interaction between components

# - Rendering Engine

# - Data Engine

food_to_survive = 2

class EvolSim:
	def __init__(self, animal_num=200, food_num=200, world_dim=(20,20), day_len=20):
		print("Initializing simulation")
		self.food_num = food_num
		self.animal_num = animal_num
		self.world_x, self.world_y = world_dim
		self.day_len = day_len
		self.worldFood = [[0 for i in range(self.world_y)] for j in range(self.world_x)]
		self.generate_world(animal_num, food_num)
	
	def run(self, num_iter=1): 
		print("Running simulation for " + str(num_iter))
		time = 0
		for i in range(0,num_iter):
			self.update_animal_pos()
			self.consume_food()
			time += 1
			if(time == self.day_len):
				surviving_animals = sum(2 if a.can_reproduce() else 1 if a.can_survive() else 0 for a in self.animals)
				print(str(surviving_animals) + " survived!")
				self.generate_world(surviving_animals, self.food_num)

				ui_api.update_plot(surviving_animals)
				time = 0

	# 0.0.0 move animals in a random direction (4-way) with constant step
	def update_animal_pos(self):
		for a in self.animals:
			a.move(self.world_x, self.world_y)

	# 0.0.0 consume food on a first come first serve basis
	def consume_food(self):
		for a in self.animals:
			if self.worldFood[a.posX][a.posY] > 0:
				self.worldFood[a.posX][a.posY] -= 1
				a.eat()

	def generate_world(self, num_animal, num_food):
		self.generate_foods(num_food)
		self.generate_animals(num_animal)

	# 0.0.0 amount of food is replenished to the same contstant amount
	def generate_foods(self, num):
		new_food_pos = random.sample(range(0,self.world_x * self.world_y), num)
		for n in new_food_pos:
			self.worldFood[int(math.floor(n/self.world_y))][n%self.world_y] += 1

	def generate_animals(self, num):
		new_animal_pos = random.sample(range(0,self.world_x * self.world_y), num)
		self.animals = list(map(lambda n: Animal(int(math.floor(n/self.world_y)), n % self.world_y), new_animal_pos))

