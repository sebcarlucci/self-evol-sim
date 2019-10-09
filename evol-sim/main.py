# main.py
import json
from evol_sim import SimEngineThread
from ui_engine_api import UIThread
import time
from async_msg import AsyncMsgController
from async_msg import AsyncMsgEvents as async_events

DEF_CONFIG_FILE = "./config.json"

def init_sys(msg_controller, config=None):
	ui_op = msg_controller.build_operator('UI-Engine')
	sim_op = msg_controller.build_operator('Sim-Engine')

	sim_thread = SimEngineThread(sim_op, msg_controller)
	ui_thread = UIThread(ui_op, msg_controller)

	ui_thread.start()
	sim_thread.start()
	msg_controller.send_to('Sim-Engine', (async_events.SimEngineEvents.start,100))
	time.sleep(1)

def main():
	name = "evol_sim"
	ver = "0.0.0"
	print(name + " " + ver)

	msg_controller = AsyncMsgController()
	init_sys(msg_controller=msg_controller)

	msg_controller.start()

main()
