from typing import List
from color import Color
from state import State
import numpy as np
from abc import ABC

class Node:
    
    _random_state = 0 
    
    def __init__(self, state: State) -> None:
        self.state = state
        self.color = self._color_from_state()
    
    def __hash__(self) -> int:
        return self.state.__hash__()
    
    def _color_from_state(self) -> Color:
        rand = np.random.RandomState(self.state.value + self._random_state)
        return Color(rand.randint(0, 4, 1))
    
    @classmethod
    def set_random_state(cls, random_state: int):
        cls._random_state = random_state
    
class ColorGraph(ABC):
    def __init__(self):
        self._graph: dict[Node, List[Node]] = None
    
    def to_array(self):
        dim = max([key.state.value for key in self._graph.keys()]) + 1
        array = np.full((dim, dim), np.nan)
        for key, nodes in self._graph.items():
            array[key.state.value][key.state.value] = key.color.value
            for node in nodes:
                array[key.state.value][node.state.value] = node.color.value
        return array
    

class BrazilGraph(ColorGraph):
    def __init__(self, random_state: int):
        Node.set_random_state(random_state)
        self._graph = {
            Node(State.RN): [Node(State.PB), Node(State.CE)],
            Node(State.PB): [Node(State.RN), Node(State.CE), Node(State.PE)],
            Node(State.CE): [Node(State.RN), Node(State.PB), Node(State.PE), Node(State.PI)],
            Node(State.PE): [Node(State.PB), Node(State.CE), Node(State.PI), Node(State.BA), Node(State.AL)],
            Node(State.AL): [Node(State.PE), Node(State.SE), Node(State.BA)],
            Node(State.SE): [Node(State.AL), Node(State.BA)],
            Node(State.PI): [Node(State.CE), Node(State.PE), Node(State.MA), Node(State.TO), Node(State.BA)],
            Node(State.BA): [Node(State.SE), Node(State.AL), Node(State.PE), Node(State.PI), Node(State.TO), Node(State.GO), Node(State.ES)],
            Node(State.ES): [Node(State.BA), Node(State.MG), Node(State.RJ)],
            Node(State.DF): [Node(State.GO)],
            Node(State.MA): [Node(State.PI), Node(State.PA), Node(State.TO)],
            Node(State.TO): [Node(State.PI), Node(State.MA), Node(State.PA), Node(State.MT), Node(State.GO), Node(State.BA)],
            Node(State.GO): [Node(State.BA), Node(State.TO), Node(State.MT), Node(State.MS), Node(State.MG), Node(State.DF)],
            Node(State.MG): [Node(State.BA), Node(State.ES), Node(State.RJ), Node(State.SP), Node(State.MS), Node(State.GO)],
            Node(State.RJ): [Node(State.ES), Node(State.MG), Node(State.SP)],
            Node(State.PA): [Node(State.MA), Node(State.TO), Node(State.MT), Node(State.AM), Node(State.RR), Node(State.AP)],
            Node(State.MT): [Node(State.TO), Node(State.GO), Node(State.MS), Node(State.RO), Node(State.AM), Node(State.PA)],
            Node(State.MS): [Node(State.MG), Node(State.GO), Node(State.MT), Node(State.SP), Node(State.PR)],
            Node(State.SP): [Node(State.MG), Node(State.RJ), Node(State.MS), Node(State.PR)],
            Node(State.RR): [Node(State.PA), Node(State.AM)],
            Node(State.AP): [Node(State.PA)],
            Node(State.PR): [Node(State.MS), Node(State.SP), Node(State.SC)],
            Node(State.AM): [Node(State.PA), Node(State.RR), Node(State.AC), Node(State.RO), Node(State.MT)],
            Node(State.RO): [Node(State.MT), Node(State.AM), Node(State.AC)],
            Node(State.AC): [Node(State.AM), Node(State.RO)],
            Node(State.SC): [Node(State.PR), Node(State.RS)],
            Node(State.RS): [Node(State.SC)],
        }
                    
