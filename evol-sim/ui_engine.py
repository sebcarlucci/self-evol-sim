# ui-engine.py

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang.builder import Builder

from kivy.graphics import Rectangle

import threading
import random

def test(dt):
	threading.current_thread().async_msg_thread_ref.send_msg('Sim-Engine', (1,100))

class MainApp(App):
	def build(self):
		return Builder.load_file("./widgets/main.kv")

class PlotComponent(Rectangle):

	def __init__(self,**kwargs):
		if not any(k in kwargs.keys() for k in ['id', 'val']):
			raise IllegalArgumentError()

		self.val = kwargs['val']
		del kwargs['val']
		print(self.val)
		super(PlotComponent, self).__init__(**kwargs)

class Plot(StackLayout):
	values = ObjectProperty()
	id_cnt = 0
	ids = {}
	max_val = NumericProperty(0)
	value_cnt = NumericProperty(0)

	def config(self, num_values):
		self.value_cnt = num_values

	def add_element(self, val):
		if val > self.max_val:
			self.max_val = val
		# Add new plot component
		new_plot_id = self.id_cnt
		with self.canvas:
			self.ids[new_plot_id] = PlotComponent(size=(self.width/self.value_cnt, self.height * val / self.max_val), \
											      id=self.id_cnt, val=val,                                            \
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

	def on_touch_down(self, pos):
		self.value_cnt += 100
		for child in self.ids.values():
			child.size_hint_x = 1/self.value_cnt
		# Clock.schedule_once(test, 1)
		test(0)
		return True

class RootLayout(BoxLayout):
	pass

if __name__ == '__main__':
	MainApp().run()	
