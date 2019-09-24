# evol_sim.py
import random

class EvolSim:
	def __init__(self, animal_pos, food_pos, world_dim):
		self.animal_pos = animal_pos
		self.food_pos = food_pos
		w, h = world_dim["x"], world_dim["y"]
		self.world = [['O' for x in range(w)] for y in range(h)]
		for a in animal_pos:
			a["food"] = 0
			self.world[a["x"]][a["y"]]= "A"
		for f in food_pos:
			self.world[f["x"]][f["y"]]= "F"
		self.day_len = 20
		self.time = 0
	
	def run(self, num_iter=1): 
		for i in range(0,num_iter):
			self.update_animal_pos()
			self.consume_food()
			self.time += 1
			if(self.time == self.day_len):
				self.generate()

	def update_animal_pos(self):
		for a in self.animal_pos:
			flag = random.randint(0,2)
			pos = random.randint(0,1)
			if(flag is 1):
				a["x"] += 1 if pos is 1 else -1
			else:
				a["y"] += 1 if pos is 1 else -1

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

