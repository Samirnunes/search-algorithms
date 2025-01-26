import numpy as np
from particle import ColorParticle
from graph import BrazilGraph
from state import State
from color import Color
from fitness import MIN_FITNESS
from logging import getLogger
from logging import StreamHandler
from logging import INFO
import matplotlib.pyplot as plt
import networkx as nx
import sys


class QuaternaryPSO:
    _random_state = 0

    def __init__(
        self,
        n_particles: int = 20,
        w_max: float = 2.0,
        w_min: float = 0.8,
        c1: float = 2.0,
        c2: float = 1.8,
        max_iter: int = 10000,
    ):
        assert w_min < w_max

        self._logger = getLogger(self.__class__.__name__)
        self._logger.setLevel(INFO)
        self._logger.addHandler(StreamHandler(sys.stdout))

        self._particles = [
            ColorParticle.from_graph(BrazilGraph(i)) for i in range(n_particles)
        ]
        self._best = self._particles[0].best
        for particle in self._particles:
            self._update_best(particle, 0)
        self._w = w_max
        self._w_max = w_max
        self._w_min = w_min
        self._c1 = c1
        self._c2 = c2
        self._max_iter = max_iter
        self._r = 0.5

    def run(self):
        iter_count = 0
        while iter_count < self._max_iter and self._best.fitness > MIN_FITNESS:
            self._update_w(iter_count)
            for i in range(len(self._particles)):
                self._update_particle(self._particles[i])
                self._update_best(self._particles[i], iter_count)
            iter_count += 1
        self._plot_best()
        return self._get_result()

    def _get_result(self):
        result: dict[State, Color] = {}
        for i in range(self._best.position.shape[0]):
            result[State(i)] = Color(self._best.position[i][i])
        return result, self._best.fitness

    def _plot_best(self):
        matrix = self._best.position
        color_map = {-1: "gray", 0: "red", 1: "blue", 2: "green", 3: "yellow"}
        G = nx.Graph()
        node_colors = []
        for i in range(matrix.shape[0]):
            node_color = color_map[matrix[i, i]]
            node_colors.append(node_color)
            G.add_node(State.map(i), color=node_color)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i, j] >= 0 and j != i:
                    G.add_edge(State.map(i), State.map(j))
        plt.figure(figsize=(20, 12))
        pos = nx.kamada_kawai_layout(G)
        nx.draw_networkx_nodes(
            G, pos, node_color=node_colors, node_size=500, edgecolors="black"
        )
        nx.draw_networkx_edges(G, pos, width=1.5)
        nx.draw_networkx_labels(G, pos, font_color="black")
        plt.show()

    def _update_particle(self, particle: ColorParticle):
        def f(velocity: np.float64, rand: np.float64):
            def sigmoid(v: np.float64):
                return 1 / (1 + np.exp(-v))

            sig_velocity = sigmoid(velocity)
            if rand > self._r and rand < sig_velocity:
                return 0
            if rand < self._r and rand < sig_velocity:
                return 1
            if rand <= self._r and rand >= sig_velocity:
                return 2
            return 3

        rand = self._rand_const()
        new_velocity = np.where(
            particle.position != np.nan,
            np.clip(
                (
                    self._w * particle.velocity
                    + self._c1 * rand * (particle.best.position - particle.position)
                    + self._c2 * rand * (self._best.position - particle.position)
                ),
                -3,
                3,
            ),
            np.nan,
        )

        new_position = np.where(
            particle.position is not np.nan,
            (particle.position + np.vectorize(f)(new_velocity, rand)) % 4,
            np.nan,
        )

        particle.update(new_position, new_velocity)

    def _update_best(self, particle: ColorParticle, iter_count: int):
        if particle.best.fitness < self._best.fitness:
            self._best = particle.best
            self._logger.info(
                f"At iteration {iter_count}, best global fitness = {self._best.fitness}"
            )

    def _update_w(self, iter_count: int):
        self._w = (
            self._w_max - iter_count * (self._w_max - self._w_min) / self._max_iter
        )

    @classmethod
    def _rand_const(cls):
        rand = np.random.RandomState(cls._random_state)
        cls._random_state += 1
        return rand.uniform(0, 1, 1)
