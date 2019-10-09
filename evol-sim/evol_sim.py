# evol_sim.py
import random
import math
from animals import Animal
import threading
import time
from async_msg import AsyncMsgThread, send_msg_to_controller
from async_msg import AsyncMsgEvents as async_events

# - Day Engine -> night and day logic
# - Physics Engine
#    -> animals
#    -> phyisical interaction between components

# - Rendering Engine

# - Data Engine

food_to_survive = 2

class EvolSim:
	'''
		animal_num: number of animals initially in the Sim
		food_num: amount of food initially in Sim
		world_dim: dimensions of the 2D gird where the simulations happens
		day_len: number of days the animals have to look for food
		render_intvl: defines after how many days the Simulation UI gets updated
	'''
	def __init__(self, animal_num=2, food_num=30, world_dim=(50,50), day_len=200, render_intvl=20):
		print("Initializing simulation")
		self.food_num = food_num
		self.animal_num = animal_num
		self.world_dim = world_dim
		self.world_x, self.world_y = world_dim
		self.day_len = day_len
		self.render_intvl = render_intvl
		self.world_food = [[0 for i in range(self.world_y)] for j in range(self.world_x)]
		self.generate_world(animal_num, food_num)
	
	'''
	Day Engine
	'''
	def run(self, num_iter=1): 
		print("Running simulation for " + str(num_iter))
		num_days = num_iter
		tick_till_render = self.render_intvl
		send_msg_to_controller('UI-Engine', (async_events.UIEngineEvents.config_sim_ui,self.world_dim))
		for i in range(0,num_days):
			self.run_day()

			surviving_animals = sum(2 if a.can_reproduce() else 1 if a.can_survive() else 0 for a in self.animals)
			self.generate_world(surviving_animals, self.food_num)

			send_msg_to_controller('UI-Engine', (async_events.UIEngineEvents.add_plot_element,surviving_animals), log=False)

			tick_till_render -= 1
			if tick_till_render == 0:
				tick_till_render = self.render_intvl
				# send_msg_to_controller('UI-Engine', (async_events.UIEngineEvents.register_movement, (self.animals, self.world_food)), log=False)


	def run_day(self):
		for tick in range(0,self.day_len):
			self.update_animal_pos()
			self.consume_food()
			send_msg_to_controller('UI-Engine', (async_events.UIEngineEvents.register_movement, (self.animals, self.world_food)), log=False, time_sleep=5/200)

	# 0.0.0 move animals in a random direction (4-way) with constant step
	def update_animal_pos(self):
		for a in self.animals:
			a.move(self.world_x, self.world_y)

	# 0.0.0 consume food on a first come first serve basis
	def consume_food(self):
		for a in self.animals:
			if self.world_food[int(a.posX)][int(a.posY)] > 0:
				self.world_food[int(a.posX)][int(a.posY)] -= 1
				a.eat()

	def generate_world(self, num_animal, num_food):
		self.generate_foods(num_food)
		self.generate_animals(num_animal)

	# 0.0.0 amount of food is replenished to the same contstant amount
	def generate_foods(self, num):
		new_food_pos = random.sample(range(0,self.world_x * self.world_y), num)
		for n in new_food_pos:
			self.world_food[int(math.floor(n/self.world_y))][n%self.world_y] += 1

	def generate_animals(self, num):
		new_animal_pos = random.sample(range(0,self.world_x * self.world_y), num)
		self.animals = list(map(lambda n: Animal(int(math.floor(n/self.world_y)), n % self.world_y), new_animal_pos))

class SimEngineThread(AsyncMsgThread):
	def __init__(self, async_msg_object, controller):
		self.sim_instance = EvolSim()
		async_msg_object.set_msg_handler(self.msg_handler)
		super().__init__(async_msg_object, controller)

	def msg_handler(self, msg):
		msg_event, msg_val = msg
		if msg_event == async_events.SimEngineEvents.start:
			# Each plot bar is a day
			send_msg_to_controller('UI-Engine', (async_events.UIEngineEvents.start, msg_val))
		elif msg_event == async_events.SimEngineEvents.run:
			self.sim_instance.run(msg_val)
		return