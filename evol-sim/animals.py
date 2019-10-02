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

	def move(self, n, m):
		flag = random.randint(0,2)
		pos = random.randint(0,1)
		if flag is 1:
			self.posX += 1 if pos is 1 else -1
		else:
			self.posY += 1 if pos is 1 else -1

		self.posX %= n
		self.posY %= m

