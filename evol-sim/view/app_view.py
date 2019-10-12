# app_view.py

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang.builder import Builder

from view.simulation_view import AnimalView, FoodView

class MainApp(App):

	def build(self):
		pass

	def add_plot_element(self, val):
		self.root.ids.data_view.ids.plot.add_element(val)

	def init_sim_view(self, world):
		self.root.ids.simulation_view.add_entities(world)

	def update_sim_view(self, world):
		self.root.ids.simulation_view.update_entities(world)

	def clear_entities(self, **kwargs):
		self.root.ids.simulation_view.clear_entities(**kwargs)

	def config_sim_ui(self, scale):
		self.root.ids.simulation_view.set_scale(scale)

	def get_current_tab(self):
		return self.root.current_tab

class RootLayout(TabbedPanel):
	pass

if __name__ == '__main__':
	MainApp().run()	
