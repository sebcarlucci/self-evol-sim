# data_view.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import Rectangle
import sys
sys.path.append('..')
from async_msg import send_msg_to_controller
from async_msg import AsyncMsgEvents as async_events

class PlotComponent(Rectangle):

	def __init__(self,**kwargs):
		if not any(k in kwargs.keys() for k in ['id', 'val']):
			raise IllegalArgumentError()

		self.val = kwargs['val']
		del kwargs['val']
		super(PlotComponent, self).__init__(**kwargs)

class Plot(StackLayout):
	values = ObjectProperty()
	id_cnt = 0
	ids = {}
	max_val = NumericProperty(-1)
	value_cnt = NumericProperty(0)

	def config(self, num_values):
		self.value_cnt = num_values

	def add_element(self, val):
		if val > self.max_val:
			self.max_val = val
		# Add new plot component
		new_plot_id = self.id_cnt
		with self.canvas:
			self.ids[new_plot_id] = PlotComponent(size=(self.width/self.value_cnt, self.height * val / self.max_val),
											      id=self.id_cnt, val=val,
											      pos=(self.id_cnt*self.width/self.value_cnt + self.x, self.y))
		self.id_cnt += 1

	def on_value_cnt(self, instance, value_cnt):
		# Update the height
		for id, child in self.ids.items():
			child.size = self.width/value_cnt, self.height * child.val / self.max_val
			child.pos = self.x + id * self.width / value_cnt, self.y

	def on_max_val(self, instance, max_val):
		for child in self.ids.values():
			child.size = child.size[0], self.height * child.val / max_val

class DataView(BoxLayout):

	def on_touch_down(self, touch):
		btn = self.ids.btn_sim
		plot = self.ids.plot
		if btn.collide_point(*touch.pos):
			plot.value_cnt += 400
			for child in plot.ids.values():
				child.size_hint_x = 1/plot.value_cnt
			send_msg_to_controller('Sim-Engine', (async_events.SimEngineEvents.run,400))
			return True
		return False
