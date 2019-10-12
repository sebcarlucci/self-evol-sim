# simulation_view.py
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import InstructionGroup
from kivy.utils import get_color_from_hex as hex
from random import randrange

class EntityColor():
	Brown=hex('#d97f09')
	Blue=hex('#4266f5')
 
class EntityView(Rectangle):
	def __init__(self, size, pos):
		super().__init__(size=size, pos=pos, group='entities')

class AnimalView(EntityView):
	rgb = EntityColor.Brown
	def __init__(self, size, pos):
		super().__init__(size=size, pos=pos)

class FoodView(EntityView):
	rgb = EntityColor.Blue
	def __init__(self, size, pos):
		super().__init__(size=size, pos=pos)

class SimulationView(Widget):
	def __init__(self, **kwargs):
		super(SimulationView, self).__init__()
		self.tmp = 0
		self.scale = self.size
		self.entity_map = {}

	def clear_entities(self, **kwargs):
		if 'list_entities' in kwargs:
			for e in kwargs['list_entities']:
				try:
					self.canvas.remove(self.entity_map[e])
					del self.entity_map[e]
				except:
					print("Warning did not find {e} in entity_map".format(e=e))
		else:
			self.canvas.remove_group('entities')

	def set_scale(self, scale):
		print("setting scale ", scale)
		self.scale = scale

	def apply_scale(self, pos):
		return pos[0] * self.width/self.scale[0], pos[1] * self.height/self.scale[1]

	def add_entities(self, world):
		with self.canvas:
			for chunk_row in world.chunks:
				for chunk in chunk_row:
					chunk.thread_lock.acquire(True)

					# Add animals to canvas
					animals = chunk.animals
					Color(rgb=AnimalView.rgb)
					for e in animals:
						pos = e.get_pos()
						pos = (pos[0] + chunk.pos[0] * chunk.size, pos[1] + chunk.pos[1] * chunk.size)
						self.entity_map[e] = AnimalView(size=(5,5), pos=self.apply_scale(pos))
					# Add foods to canvas
					foods = chunk.foods
					Color(rgb=FoodView.rgb)
					for f in foods:
						pos = f.get_pos()
						pos = (pos[0] + chunk.pos[0] * chunk.size, pos[1] + chunk.pos[1] * chunk.size)
						self.entity_map[f] = FoodView(size=(5,5), pos=self.apply_scale(pos))

					chunk.thread_lock.release()

	def update_entities(self, world):
		for chunk_row in world.chunks:
			for chunk in chunk_row:
				chunk.thread_lock.acquire(True)

				# Update animals on canvas
				animals = chunk.animals
				for e in animals:
					pos = e.pos
					pos = (pos[0] + chunk.pos[0] * chunk.size, pos[1] + chunk.pos[1] * chunk.size)
					self.entity_map[e].pos = self.apply_scale(pos)
				# Update food on canvas
				foods = chunk.foods
				for f in foods:
					pos = f.pos
					pos = (pos[0] + chunk.pos[0] * chunk.size, pos[1] + chunk.pos[1] * chunk.size)
					self.entity_map[f].pos = self.apply_scale(pos)

				chunk.thread_lock.release()

