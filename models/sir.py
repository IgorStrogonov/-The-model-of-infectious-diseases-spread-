import numpy as np
import simpy

from models.agents import BaseAgent


class SIRBasicAgent(BaseAgent):
    def __init__(self, env: simpy.Environment, name: str, beta: float, gamma: float):
        super().__init__(env=env, name=name)
        self.beta: float = beta
        self.gamma: float = gamma
        self.is_susceptible: bool = True
        self.is_infected: bool = False
        self.is_resistant: bool = False

    def run(self):
        while True:
            if self.is_susceptible:
                got_infected: bool = bool(np.random.binomial(n=1, p=self.beta))
                if got_infected:
                    self.is_infected = True
                    self.is_susceptible = False
                yield self.env.timeout(1)

            if self.is_infected:
                got_resistant: bool = bool(np.random.binomial(n=1, p=self.gamma))
                if got_resistant:
                    self.is_resistant = True
                    self.is_infected = False
                yield self.env.timeout(1)

            if self.is_resistant:
                yield self.env.timeout(1)
