
import json
import random
import zoneinfo
from datetime import datetime
from typing import Dict

import simpy

from metrics.sir import SIRMetricsCollector
from models.sir import SIRBasicAgent

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--output_path", "-o", 
    type=str, 
    default="simulation_data", 
    help="Simulation output folder"
)

parser.add_argument(
    "--random_seed", "-r",
    type=int, 
    default=42, 
    help="Random seed"
)

parser.add_argument(
    "--beta", "-b", 
    type=float, 
    default=0.025,
    help="Model parameter 'beta'"
)

parser.add_argument(
    "--gamma", "-g", 
    type=float, 
    default=0.01,
    help="Model parameter 'gamma'"
)

parser.add_argument(
    "--n_agents", "-n", 
    type=int, 
    default=100,
    help="Agent count"
)

parser.add_argument(
    "--sim_time", "-t", 
    type=int, 
    default=365,
    help="Sim duration, units"
)

parser.add_argument(
    "--config_path", "-c", 
    type=str, 
    default="simulation_config",
    help="Config file path"
)

args = parser.parse_args()

MSK = zoneinfo.ZoneInfo("Europe/Moscow")


def msk_now_str():
    return datetime.now(MSK).strftime("%Y-%m-%d-%H%M%SZ")


RANDOM_SEED = args.random_seed
BETA = args.beta
GAMMA = args.gamma
N_AGENTS = args.n_agents
SIM_TIME = args.sim_time

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
    collector.to_csv(f"{args.output_path}/SIR_SimulationData-{simulation_ts}.csv")

    simulation_params = {
        "random_seed": RANDOM_SEED,
        "beta": BETA,
        "gamma": GAMMA,
        "n_agents": N_AGENTS,
        "sim_time": SIM_TIME,
        "simulation_ts": simulation_ts
    }

    with open(f'{args.output_path}/SIR_SimulationParams-{simulation_ts}.json', 'w') as f:
        json.dump(simulation_params, f)