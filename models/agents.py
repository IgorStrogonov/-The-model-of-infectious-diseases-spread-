from abc import ABC, abstractmethod

import simpy


class BaseAgent(ABC):
    def __init__(self, env: simpy.Environment, name: str):
        self.env = env
        self.name = name

    @abstractmethod
    def run(self):
        pass
