# ui-engine-api.py
from ui_engine import MainApp
import threading
import time

import random

ui_ref = None
class UIThread(threading.Thread):
	def run(self):
		ui_ref.run()

def start_plot(num_values):
	global ui_ref
	ui_ref = MainApp()
	UIThread().start()
	time.sleep(1)
	ui_ref.root.ids['plot'].config(num_values=num_values)

def update_plot(val):
	global ui_ref
	if ui_ref is None:
		raise NullPointerException()
	ui_ref.root.ids['plot'].add_element(val)
	time.sleep(0.01)