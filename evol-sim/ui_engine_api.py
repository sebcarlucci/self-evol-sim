# ui-engine-api.py
from view.app_view import MainApp
import threading
import time

import random

from async_msg import AsyncMsgThread
from async_msg import AsyncMsgEvents as async_events

class UIVisualThread(AsyncMsgThread):
	
	def __init__(self, ui_ref, async_msg_object, controller):
		self.ui_ref = ui_ref
		super().__init__(async_msg_object, controller)

	def run(self):
		self.ui_ref.run()

class UIThread(AsyncMsgThread):
	def __init__(self, async_msg_object, controller):
		self.ui_instance = MainApp()
		async_msg_object.handler = self.msg_handler
		super().__init__(async_msg_object, controller)

	def msg_handler(self, msg):
		msg_event, msg_val = msg
		if msg_event == async_events.UIEngineEvents.start:
			ui_visual_op = self.controller.build_operator('UI-Visual')
			UIVisualThread(self.ui_instance, ui_visual_op, self.controller).start()
			time.sleep(1) # Give time for the UI to load
			# self.ui_instance.config(num_values=msg_val)
		elif msg_event == async_events.UIEngineEvents.add_plot_element:
			self.ui_instance.add_plot_element(msg_val)
		elif msg_event == async_events.UIEngineEvents.register_movement:
			if self.ui_instance.get_current_tab().tab_id == 'tab_simulation_view':
				self.ui_instance.clear_entities()
				# self.ui_instance.add_entity(pos=msg_val[0].get_pos())
				animals, food = msg_val
				self.ui_instance.add_animal_entities(animals)
				# for a in animals:
				# 	self.ui_instance.add_animal_entities(pos=a.get_pos())
			
		elif msg_event == async_events.UIEngineEvents.config_sim_ui:
			self.ui_instance.config_sim_ui(msg_val)

		time.sleep(0)
		return