# ui-engine.py

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget

from kivy.lang.builder import Builder

import random
class MainApp(App):
	def build(self):
		return Builder.load_file("./widgets/main.kv")

class PlotComponent(Widget):

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
	max_val = NumericProperty(0)

	def config(self, num_values):
		self.value_cnt = num_values

	def add_element(self, val):
		if val > self.max_val:
			self.max_val = val
		# Add new plot component
		new_plot_id = "pc_" + str(self.id_cnt)
		new_plot = PlotComponent(size_hint=(1/self.value_cnt, 0 if self.max_val is 0 else val/self.max_val), id=new_plot_id, val=val)
		self.add_widget(new_plot)
		self.ids[new_plot_id] = new_plot
		self.id_cnt += 1

	def on_max_val(self, instance, max_val):
		print('new max')
		for child in self.ids.values():
			child.size_hint_y = child.val/max_val

class RootLayout(BoxLayout):
	pass

if __name__ == '__main__':
	MainApp().run()	
