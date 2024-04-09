from enum import Enum
from typing import List, Optional, Tuple

import networkx as nx

from simulation.graph import Node, sort_neighbors


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
        starting_node: Node,
        interval: Tuple[float, float],
    ) -> None:
        # Personal Attributes
        self.id = id
        self.algorithm = algorithm
        self.color = color
        self.interval = interval
        self.filled_interval = False

        # Algorithm Attributes
        self.known_graph = nx.Graph()
        self.finished: bool = False
        self.effective_path = []
        self.visited_path = []
        self.explored = []
        self.search = []
        self.current_node_id = None
        self.filled_interval = False

        # Start Graph
        self.starting_node = starting_node
        starting_node_id, starting_node_attrs = starting_node.node_view()
        self.known_graph.add_node(starting_node_id, **starting_node_attrs)
        self.known_graph.add_edges_from(starting_node.edges)

    def moving_algorithm(
        self, graph: nx.Graph
    ) -> Tuple[List[str], List[str], List[str], bool]:
        # Init Properties
        self.finished = False
        self.effective_path = []
        self.visited_path = []
        self.explored = [self.starting_node.id]
        self.search = []
        self.current_node_id = self.starting_node.id

        parent_list = []
        # Starting parent with invalid nodes
        parent_list.append("-1,-1")

        while True:
            node_data = graph.nodes[self.current_node_id]

            # Checking if the current node is the finish
            if node_data.get("finish"):
                self.search.append(self.current_node_id)
                self.effective_path.append(self.current_node_id)
                self.finished = True
                break

            # Fetching all neighbors that weren't explored
            non_visited_neighbors = sort_neighbors(
                [
                    neighbor
                    for neighbor in graph.neighbors(self.current_node_id)
                    if neighbor not in self.explored and neighbor != parent_list[-1]
                ],
                self.current_node_id,
            )
            count_non_visited_neighbors = len(non_visited_neighbors)

            all_neighbors = sort_neighbors(
                [
                    neighbor
                    for neighbor in graph.neighbors(self.current_node_id)
                    if neighbor != parent_list[-1]
                ],
                self.current_node_id,
            )

            # No more neighbors to visit, go back
            if count_non_visited_neighbors == 0:
                # Consider current cell explored
                if self.current_node_id not in self.explored:
                    self.explored.append(self.current_node_id)

                self.search.append(self.current_node_id)

                # After searching everybody and going back to root, stop
                if self.current_node_id == self.starting_node.id:
                    break

                self.current_node_id = parent_list.pop()
                self.effective_path.pop()
                self.visited_path.pop()

                continue

            # Defining next neighbor( Returning -1 should go back)
            next_neighbor_id = self.define_agent_next_step(
                all_neighbors=all_neighbors,
                non_visited_neighbors=non_visited_neighbors,
            )

            # No valid neighbor
            if next_neighbor_id == "-1":
                # Consider current cell explored
                if self.current_node_id not in self.explored:
                    self.explored.append(self.current_node_id)

                self.search.append(self.current_node_id)

                if self.current_node_id != self.starting_node.id:
                    self.current_node_id = parent_list.pop()
                    self.effective_path.pop()
                    self.visited_path.pop()
                continue

            if self.current_node_id not in self.explored:
                self.explored.append(self.current_node_id)

            parent_list.append(self.current_node_id)
            self.search.append(self.current_node_id)
            self.effective_path.append(self.current_node_id)
            self.current_node_id = next_neighbor_id

        return self.search, self.effective_path, self.explored, self.finished

    def define_agent_next_step(
        self,
        all_neighbors: List[str],
        non_visited_neighbors: List[str],
    ) -> str:
        total_number_of_neighbors = len(all_neighbors)

        if total_number_of_neighbors == 1:
            self.visited_path.append((-1, -1))
            return all_neighbors[0]

        relative_node_weights = self.get_relative_node_weights(
            total_number_of_neighbors
        )

        if self.filled_interval == False:
            for i in range(total_number_of_neighbors):
                if self.interval[1] <= relative_node_weights[i][0]:
                    self.filled_interval = True
                    break

                node_is_inside_agent_interval = (
                    self.interval[0] < relative_node_weights[i][1]
                    and self.interval[1] > relative_node_weights[i][0]
                )

                non_visited_node = all_neighbors[i] in non_visited_neighbors

                if node_is_inside_agent_interval and non_visited_node:
                    self.visited_path.append((i, total_number_of_neighbors))
                    return all_neighbors[i]

            if self.current_node_id == self.starting_node.id:
                self.filled_interval = True

            if self.filled_interval == False:
                return "-1"

        for i in range(total_number_of_neighbors):
            if all_neighbors[i] in non_visited_neighbors:
                self.visited_path.append((i, total_number_of_neighbors))
                return all_neighbors[i]

    def get_relative_node_weights(
        self, count_neighbors: int
    ) -> List[Tuple[float, float]]:
        path_size = len(self.visited_path)
        node_interval = (0, 1)

        # Calculate relative node weights based on agent path
        if path_size > 0:
            if self.visited_path[0][0] != -1:
                chunk = 1 / self.visited_path[0][1]

                node_interval = (
                    self.visited_path[0][0] * chunk,
                    self.visited_path[0][0] * chunk + chunk,
                )

            for i in range(1, path_size):
                if self.visited_path[i][0] == -1:
                    continue

                node_interval_size = node_interval[1] - node_interval[0]
                chunk = node_interval_size / self.visited_path[i][1]
                node_interval = (
                    node_interval[0] + self.visited_path[i][0] * chunk,
                    node_interval[0] + self.visited_path[i][0] * chunk + chunk,
                )

        # Calculate weights of the next nodes
        weights = []
        node_interval_size = node_interval[1] - node_interval[0]
        chunk = node_interval_size / count_neighbors
        start = 0
        end = 0

        for i in range(count_neighbors):
            start = node_interval[0] + chunk * i
            end = start + chunk
            weight = (start, end)
            weights.append(weight)

        return weights

    def move(self, graph: nx.Graph) -> Tuple[List[str], List[str], List[str], bool]:
        if self.algorithm == Algorithm.SELF.value:
            return self.moving_algorithm(graph=graph)
