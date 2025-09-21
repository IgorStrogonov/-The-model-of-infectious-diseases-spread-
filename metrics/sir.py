from typing import List

import pandas as pd
import simpy

from metrics.collector import BaseMetricsCollector
from models.sir import SIRBasicAgent


class SIRMetricsCollector(BaseMetricsCollector):
    def __init__(self, env: simpy.Environment, entities: List[SIRBasicAgent]):
        super().__init__(env=env, entities=entities)

    def _collect_metrics(self):
        return {
            "time": self.env.now,
            "susceptible": sum([int(a.is_susceptible) for a in self.entities]),
            "infected": sum([int(a.is_infected) for a in self.entities]),
            "resistant": sum([int(a.is_resistant) for a in self.entities]),
        }

    def get_metrics(self) -> pd.DataFrame:
        return pd.DataFrame(self._metrics_container)
