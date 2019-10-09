# simulation_view.py
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import InstructionGroup
from kivy.utils import get_color_from_hex as hex
from random import randrange

class EntityColor():
	Brown=hex('#d97f09')
	Blue=hex('#34ebe1')
 
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

	def clear_entities(self):
		self.canvas.remove_group('entities')

	def set_scale(self, scale):
		self.scale = scale

	def add_entities(self, type, entities):
		with self.canvas:
			Color(rgb=type.rgb)
			for e in entities:
				pos = e.get_pos()
				type(size=(5,5), pos=(pos[0]*self.width/self.scale[0], pos[1]*self.height/self.scale[1]))
