# ui-engine.py

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty
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
	value_cnt = 0
	ids = {}

	def on_action(self):
		self.value_cnt += 1
		for i in range(0,len(self.ids)):
			self.ids["pc_" + str(i)].size_hint_x = 1/self.value_cnt

		# Add new plot component
		new_plot_id = "pc_" + str(self.id_cnt)
		new_plot = PlotComponent(size_hint_x=1/self.value_cnt, id=new_plot_id, val=random.randint(0,int(self.height * 0.9)))
		self.add_widget(new_plot)
		self.ids[new_plot_id] = new_plot
		self.id_cnt += 1

	def add_element(self, val):
		self.value_cnt += 1
		for i in range(0,len(self.ids)):
			self.ids["pc_" + str(i)].size_hint_x = 1/self.value_cnt

		# Add new plot component
		new_plot_id = "pc_" + str(self.id_cnt)
		new_plot = PlotComponent(size_hint_x=1/self.value_cnt, id=new_plot_id, val=val)
		self.add_widget(new_plot)
		self.ids[new_plot_id] = new_plot
		self.id_cnt += 1


class RootLayout(BoxLayout):
	pass

if __name__ == '__main__':
	MainApp().run()	
