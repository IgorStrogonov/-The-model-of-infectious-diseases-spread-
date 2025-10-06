import json
import random
import zoneinfo
from datetime import datetime
from typing import Dict

import simpy

from metrics.sir import SIRMetricsCollector
from models.sir import SIRBasicAgent

import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

MSK = zoneinfo.ZoneInfo("Europe/Moscow")


def msk_now_str():
    return datetime.now(MSK).strftime("%Y-%m-%d-%H%M%SZ")


RANDOM_SEED = 42
BETA = 0.025
GAMMA = 0.01
N_AGENTS = 1000
SIM_TIME = 365

random.seed(RANDOM_SEED)

if __name__ == '__main__':
    logger.info(
        f"Simulation has started with params: --random_seed {RANDOM_SEED} --beta {BETA} --gamma {GAMMA} --n_agents {N_AGENTS} --sim_time {SIM_TIME}"
    )
    start = time.time()

    env = simpy.Environment()
    agents: Dict[int, SIRBasicAgent] = {
        n: SIRBasicAgent(env=env, name=f"A_{n}", beta=BETA, gamma=GAMMA)
        for n in range(N_AGENTS)}

    collector: SIRMetricsCollector = SIRMetricsCollector(env, list(agents.values()))

    for a in agents.values():
        env.process(a.run())

    env.process(collector.run())

    env.run(until=SIM_TIME)

    finish = time.time()
    logger.info(f"Simulation has finished. Elapsed time {(finish - start):.3f} seconds.")

    simulation_ts = msk_now_str()
    collector.to_csv(f"simulation_data/SIR_SimulationData-{simulation_ts}.csv")

    simulation_params = {
        "random_seed": RANDOM_SEED,
        "beta": BETA,
        "gamma": GAMMA,
        "n_agents": N_AGENTS,
        "sim_time": SIM_TIME,
        "simulation_ts": simulation_ts
    }

    with open(f'simulation_data/SIR_SimulationParams-{simulation_ts}.json', 'w') as f:
        json.dump(simulation_params, f)
