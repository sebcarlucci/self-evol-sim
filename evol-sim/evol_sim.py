# evol_sim.py
import random
import math
from animals import Animal
import threading
import time
from async_msg import AsyncMsgThread

# - Day Engine -> night and day logic
# - Physics Engine
#    -> animals
#    -> phyisical interaction between components

# - Rendering Engine

# - Data Engine

food_to_survive = 2

def send_msg_to_thread(id, msg):
	threading.current_thread().send_msg("UI-Engine", msg)

class EvolSim:
	def __init__(self, animal_num=200, food_num=600, world_dim=(200,200), day_len=20):
		print("Initializing simulation")
		self.food_num = food_num
		self.animal_num = animal_num
		self.world_x, self.world_y = world_dim
		self.day_len = day_len
		self.worldFood = [[0 for i in range(self.world_y)] for j in range(self.world_x)]
		self.generate_world(animal_num, food_num)
	
	'''
	Day Engine
	'''
	def run(self, num_iter=1): 
		print("Running simulation for " + str(num_iter))
		num_days = num_iter	
		for i in range(0,num_days):
			self.run_day()

	def run_day(self):
		for tick in range(0,self.day_len):
			self.update_animal_pos()
			self.consume_food()

		surviving_animals = sum(2 if a.can_reproduce() else 1 if a.can_survive() else 0 for a in self.animals)
		self.generate_world(surviving_animals, self.food_num)

		send_msg_to_thread(0, (1,surviving_animals))

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

class SimEngineThread(AsyncMsgThread):
	def __init__(self, async_msg_object, controller):
		self.sim_instance = EvolSim()
		async_msg_object.handler = self.msg_handler
		super().__init__(async_msg_object, controller)

	def msg_handler(self, msg):
		msg_id, msg_val = msg
		if msg_id == 0:
			# Each plot bar is a day
			send_msg_to_thread(0, (-1, 100))
			return
		self.sim_instance.run(100)