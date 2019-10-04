# ui-engine-api.py
from ui_engine import MainApp
import threading
import time

import random

from async_msg import AsyncMsgThread

class UIVisualThread(threading.Thread):
	
	def __init__(self, ui_ref, async_msg_thread_ref):
		self.ui_ref = ui_ref
		self.async_msg_thread_ref = async_msg_thread_ref
		super().__init__()

	def send_msg(self, id, msg):
		self.async_msg_thread_ref.send(id, msg)


	def run(self):
		self.ui_ref.run()

class UIThread(AsyncMsgThread):
	def __init__(self, async_msg_object, controller):
		self.ui_instance = MainApp()
		async_msg_object.handler = self.msg_handler
		super().__init__(async_msg_object, controller)

	def msg_handler(self, msg):
		if msg is -1:
			UIVisualThread(self.ui_instance, self).start()
			time.sleep(1) # Give the for the UI to load
			self.ui_instance.root.ids['plot'].config(num_values=5)
		else:
			self.ui_instance.root.ids['plot'].add_element(msg)