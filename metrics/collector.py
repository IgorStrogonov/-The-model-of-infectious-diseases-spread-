from abc import ABC, abstractmethod
from typing import List

import pandas as pd
import simpy


class BaseMetricsCollector(ABC):
    def __init__(self, env: simpy.Environment, entities: List):
        self.env = env
        self.entities = entities
        self._metrics_container: List = []

    def run(self):
        while True:
            metrics = self._collect_metrics()
            self._metrics_container.append(metrics)
            yield self.env.timeout(1)

    @abstractmethod
    def _collect_metrics(self) -> dict:
        pass

    @abstractmethod
    def get_metrics(self) -> pd.DataFrame:
        pass

    def to_csv(self, filename: str) -> None:
        df: pd.DataFrame = self.get_metrics()
        df.to_csv(filename, index=False)
