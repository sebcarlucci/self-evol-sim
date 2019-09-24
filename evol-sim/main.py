# main.py
import json
from evol_sim import EvolSim

DEF_CONFIG_FILE = "./config.json"

def main():
	name = "evol_sim"
	ver = "1.0.0"
	print(name + " " + ver)

	with open(DEF_CONFIG_FILE) as config_json_file:
		user_config = json.load(config_json_file)
		evol_sim = EvolSim(user_config["posAnimal"], user_config["posFood"], user_config["worldDim"])
		evol_sim.run(2)

main()