# evol_sim.py
import random
import math
from animals import Animal
import threading
import time
from async_msg import AsyncMsgThread, send_msg_to_controller
from async_msg import AsyncMsgEvents as async_events

from environment import Environment
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
	def __init__(self, animal_num=10, food_num=200, world_dim=(6,6), day_len=100, render_intvl=20):
		print("Initializing simulation")
		self.food_num = food_num
		self.animal_num = animal_num
		self.world_dim = world_dim
		self.world_x, self.world_y = world_dim
		self.day_len = day_len
		self.render_intvl = render_intvl

		self.world = Environment(self.world_x, self.world_y, 30)
		self.world.generate(animal_num, food_num)
	
	'''
	Day Engine
	'''
	def run(self, num_iter=1): 
		print("Running simulation for " + str(num_iter))
		num_days = num_iter
		tick_till_render = self.render_intvl
		send_msg_to_controller('UI-Engine', (async_events.UIEngineEvents.config_sim_ui,(self.world_dim[0] * self.world.chunk_size, self.world_dim[1] * self.world.chunk_size)))
		for i in range(0,num_days):

			start = time.time()
			self.run_day()
			run_day_elapsed_time = time.time() - start

			surviving_animals, surviving_foods= self.world.regenerate()

			print("Day {day} stats: surviving_animals: {surviving_animals} surviving_foods: {surviving_foods} elapsed_time: {elapsed_time}".format(
				day=i, 
				surviving_animals=surviving_animals, 
				surviving_foods=surviving_foods, 
				elapsed_time=run_day_elapsed_time
				)
			)
			send_msg_to_controller(
							id='UI-Engine', 
							msg=(async_events.UIEngineEvents.add_plot_element,surviving_animals), 
							log=False
			)
			send_msg_to_controller(
							id='UI-Engine', 
							msg=(async_events.UIEngineEvents.register_sim_clear_all,None), 
							log=False
			)

			tick_till_render -= 1
			if tick_till_render == 0:
				tick_till_render = self.render_intvl
				# send_msg_to_controller('UI-Engine', (async_events.UIEngineEvents.register_movement, (self.animals, self.world_food)), log=False)


	def run_day(self):
		send_msg_to_controller('UI-Engine', (async_events.UIEngineEvents.register_sim_add, self.world), log=False, time_sleep=5/200)
		for tick in range(0,self.day_len):
			eaten_foods = self.world.update()

			send_msg_to_controller(
				id='UI-Engine', 
				msg=(async_events.UIEngineEvents.register_sim_clear, eaten_foods), 
				log=False, 
				time_sleep=0
			)
			send_msg_to_controller(
				id='UI-Engine', 
				msg=(async_events.UIEngineEvents.register_sim_update, self.world), 
				log=False, 
				time_sleep=5/200
			)

	# 0.0.0 consume food on a first come first serve basis
	def consume_food(self):
		for a in self.animals:
			if self.world_food[int(a.posX)][int(a.posY)] > 0:
				self.world_food[int(a.posX)][int(a.posY)] -= 1
				a.eat()

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
