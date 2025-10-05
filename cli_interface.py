import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--output_path", "-o", 
    type=str, 
    default="simulation_data", 
    help="Simulation output folder",
    description="Путь к папке с результатами симуляции"
)

parser.add_argument(
    "--random_seed", "-r",
    type=int, 
    default=42, 
    help="Random seed", 
    description="Random seed"
)

parser.add_argument(
    "--beta", "-b", 
    type=float, 
    default=0.025,
    help="Model parameter 'beta'", 
    description="Параметр β"
)

parser.add_argument(
    "--gamma", "-g", 
    type=float, 
    default=0.01,
    help="Model parameter 'gamma'", 
    description="Параметр γ"
)

parser.add_argument(
    "--n_agents", "-n", 
    type=int, 
    default=100,
    help="Agent count",
    description="Количество агентов"
)

parser.add_argument(
    "--sim_time", "-t", 
    type=int, 
    default=365,
    help="Sim duration, units",
    description="Продолжительность симуляции, ед. времени"
)

parser.add_argument(
    "--config_path", "-c", 
    type=str, 
    default="simulation_config",
    help="Config file path",
    description="Путь к файлу конфигурации"
)

args = parser.parse_args()
