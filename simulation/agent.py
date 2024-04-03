from enum import Enum
from typing import List, Optional, Tuple

import networkx as nx

from simulation.graph import Node


class Algorithm(Enum):
    SELF = "self"
    TERRY = "terry"


class Color(Enum):
    """
    This class is created to use the colors easily.
    Each Color object has two color values.
    The first value is the color of the Agent and the second is the color of
    its footprint
    """

    black = ("black", "dim gray")
    red = ("red3", "tomato")
    cyan = ("cyan4", "cyan4")
    green = ("green4", "pale green")
    blue = ("DeepSkyBlue4", "DeepSkyBlue2")
    yellow = ("yellow2", "yellow1")
    orange = ("#f27f0c", "#f7ad19")
    pink = ("#e11584", "#f699cd")


class Agent:
    def __init__(
        self,
        id: int,
        algorithm: Algorithm,
        color: Color,
        starting_node: Optional[Node],
        interval: Tuple[float, float],
    ) -> None:
        # Personal Attributes
        self.id = id
        self.algorithm = algorithm
        self.color = color

        # Algorithm Attributes
        self.known_graph = nx.Graph()
        self.finished: bool = False
        self.visited_path = []
        self.radix_representation = 0
        self.effective_path = []
        self.explored = []
        self.search = []

        # Start Graph
        # starting_node_id, starting_node_attrs = starting_node.node_view()
        # self.known_graph.add_node(starting_node_id, **starting_node_attrs)
        # self.known_graph.add_edges_from(starting_node.edges)

    def moving_algorithm(
        self, graph: nx.Graph
    ) -> Tuple[List[str], List[str], List[str], bool]:
        return ([], [], [], False)

    def move(self, graph: nx.Graph) -> Tuple[List[str], List[str], List[str], bool]:
        print(self.algorithm)
        if self.algorithm == Algorithm.SELF.value:
            return self.moving_algorithm(graph=graph)
