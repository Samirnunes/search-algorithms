import numpy as np
from graph import ColorGraph
from fitness import fitness
from dataclasses import dataclass


@dataclass
class Best:
    position: np.ndarray
    fitness: int


class ColorParticle:
    _random_state = 0

    def __init__(self, position: np.ndarray, velocity: np.ndarray):
        self.position = position
        self.velocity = velocity
        self.best = Best(self.position, fitness(self.position))
        
    def update(self, new_position: np.ndarray, new_velocity: np.ndarray):
        self.position = new_position
        self.velocity = new_velocity
        self._update_best()
        
    def _update_best(self):
        current = fitness(self.position)
        if current < self.best.fitness:
            self.best = Best(self.position, current)

    @classmethod
    def from_graph(cls, graph: ColorGraph):
        position = graph.to_array()
        return cls(position, cls._rand_velocity(position))

    @classmethod
    def _rand_velocity(cls, position: np.ndarray):
        rand = np.random.RandomState(cls._random_state)
        cls._random_state += 1
        return np.where(position is not np.nan, rand.uniform(-1, 1, 1), np.nan)
