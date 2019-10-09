# animals.py
import random

food_to_survive = 1
class Animal():

	def __init__(self, posX, posY):
		self.posX, self.posY = posX, posY
		self.food = 0

	def can_survive(self):
		return self.food >= food_to_survive

	def can_reproduce(self):
		return self.food >= food_to_survive + 1

	def eat(self):
		self.food += 1

	def get_pos(self):
		return self.posX, self.posY

	def move(self, n, m):
		flag = random.randint(0,2)
		delta = 3*random.random()
		if flag is 1:
			self.posX += delta
		else:
			self.posY += delta
		self.posX %= n
		self.posY %= m
