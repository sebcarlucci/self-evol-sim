# main.py
import json
from evol_sim import EvolSim
import ui_engine_api as ui_api
DEF_CONFIG_FILE = "./config.json"

def main():
	name = "evol_sim"
	ver = "0.0.0"
	print(name + " " + ver)

	with open(DEF_CONFIG_FILE) as config_json_file:
		ui_api.start_plot()
		user_config = json.load(config_json_file)
		evol_sim = EvolSim()
		evol_sim.run(1000)

main()