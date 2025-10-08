import json
import random
import zoneinfo
from datetime import datetime
from typing import Dict

import simpy

from metrics.sir import SIRMetricsCollector
from models.sir import SIRBasicAgent

try:
    import tomlib
except ImportError:
    import tomli as tomlib

MSK = zoneinfo.ZoneInfo("Europe/Moscow")

def msk_now_str():
    return datetime.now(MSK).strftime("%Y-%m-%d-%H%M%SZ")

def load_config(path):
    with open(path, "rb") as f:
        conf = tomlib.load(f)
    return conf

config = load_config("config/config.toml")

RANDOM_SEED = config["random_seed"]
BETA = config["beta"]
GAMMA = config["gamma"]
N_AGENTS = config["n_agents"]
SIM_TIME = config["sim_time"]

random.seed(RANDOM_SEED)

if __name__ == '__main__':
    env = simpy.Environment()
    agents: Dict[int, SIRBasicAgent] = {
        n: SIRBasicAgent(env=env, name=f"A_{n}", beta=BETA, gamma=GAMMA)
        for n in range(N_AGENTS)}

    collector: SIRMetricsCollector = SIRMetricsCollector(env, list(agents.values()))

    for a in agents.values():
        env.process(a.run())

    env.process(collector.run())

    env.run(until=SIM_TIME)

    simulation_ts = msk_now_str()
    collector.to_csv(f"{config['output_path']}/SIR_SimulationData-{simulation_ts}.csv")

    simulation_params = {
        "random_seed": RANDOM_SEED,
        "beta": BETA,
        "gamma": GAMMA,
        "n_agents": N_AGENTS,
        "sim_time": SIM_TIME,
        "simulation_ts": simulation_ts
    }

    with open(f'{config["output_path"]}/SIR_SimulationParams-{simulation_ts}.json', 'w') as f:
        json.dump(simulation_params, f)