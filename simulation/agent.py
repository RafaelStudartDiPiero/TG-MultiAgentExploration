from enum import Enum
from typing import List, Optional, Tuple

import networkx as nx

from simulation.graph import Node, sort_neighbors
from simulation.graph_utils import display_graph, preprocess_node_ids, add_edge_to_graph


class Algorithm(Enum):
    SELF = "self"
    TERRY = "terry"


class AgentStatus(Enum):
    STARTED = "STARTING"
    SEARCHING_INTERVAL = "SEARCHING_INTERVAL"
    IN_INTERVAL = "IN_INTERVAL"
    DFS = "DFS"
    FINISHED = "FINISHED"
    STOPPED = "STOPPED"


class Color(Enum):
    """
    This class is created to use the colors easily.
    Each Color object has two color values.
    The first value is the color of the Agent and the second is the color of
    its footprint
    """

    black = ("black", "dimgray")
    red = ("red", "indianred")
    cyan = ("cyan", "darkcyan")
    green = ("green", "forestgreen")
    blue = ("blue", "royalblue")
    yellow = ("yellow", "goldenrod")
    orange = ("orange", "darkorange")
    pink = ("magenta", "orchid")


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
        # ID is the unique identification of the agent
        self.id = id
        # Algorithm defines how the agent should move
        self.algorithm = algorithm
        # Color defines the color it's path should be
        self.color = color
        # Interval defines the interval of radix values this agent will tranverse
        self.interval = interval
        # Status defines the current status of the agent
        self.status = AgentStatus.STARTED

        # Algorithm Attributes
        # Tree the represeting the agent path and decisions
        self.known_tree = nx.Graph()
        # Start Graph
        self.starting_node = starting_node
        starting_node_id, _ = starting_node.node_view()
        self.known_tree.add_node(starting_node_id)
        self.known_tree.nodes[starting_node_id]["radix"] = ("0.0", "1.0")

        # If the agent got to the final point in the graph
        self.finished: bool = False
        # The effective path taken by the agent
        self.effective_path = []
        # The radix representation of the path
        self.visited_path = []
        # The explored nodes
        self.explored = []
        # All nodes visited
        self.search = []
        # The parents of each node
        self.parent_list = ["-1,-1"]
        # The current node id
        self.current_node_id = starting_node_id
        # Check if the agent has already filled it's interval
        self.filled_interval = False
        # Agent Step Count
        self.step_count = 0

    def step_back(self):
        # Consider current cell explored
        if self.current_node_id not in self.explored:
            self.explored.append(self.current_node_id)

        self.search.append(self.current_node_id)

        # If want to go back in root, STOP or start DFS mode.
        if self.parent_list[-1] == "-1,-1":
            if (
                self.status == AgentStatus.SEARCHING_INTERVAL
                or self.status == AgentStatus.IN_INTERVAL
            ):
                print(f"This agent {self.id} search failed. Trying DFS")
                self.status = AgentStatus.DFS
                return
            if self.status == AgentStatus.DFS:
                print(f"Agent {self.id} DFS failed, stopping.")
                self.status = AgentStatus.STOPPED
                return

        # If not root, just go back
        self.current_node_id = self.parent_list.pop()
        self.effective_path.pop()
        self.visited_path.pop()
        return

    def move_one_step(self, graph: nx.Graph):
        if self.status == AgentStatus.STARTED:
            self.status = AgentStatus.SEARCHING_INTERVAL

        if self.status == AgentStatus.FINISHED:
            print(f"Agent {self.id} has already finished")
            return

        if self.status == AgentStatus.STOPPED:
            print(f"Agent {self.id} stopped before finishing")
            return

        # Check the data of the current node and add it to the known graph
        node_data = graph.nodes[self.current_node_id]
        self.known_tree.nodes[self.current_node_id]["visited"] = True
        self.known_tree.nodes[self.current_node_id]["color"] = self.color.value[1]

        # Checking if the current node is the finish
        if node_data.get("finish"):
            # If the current node is the finish, end the search
            self.search.append(self.current_node_id)
            self.effective_path.append(self.current_node_id)
            self.finished = True
            self.status = AgentStatus.FINISHED
            return

        # Fetching neighbors that weren't explored and aren't the parent of the node
        non_visited_neighbors = sort_neighbors(
            [
                neighbor
                for neighbor in graph.neighbors(self.current_node_id)
                if neighbor != self.parent_list[-1]
                and (
                    self.known_tree.nodes.get(neighbor).get("visited") != True
                    if self.known_tree.nodes.get(neighbor) is not None
                    else True
                )
            ],
            self.current_node_id,
        )
        count_non_visited_neighbors = len(non_visited_neighbors)

        # No more neighbors to visit, go back
        if count_non_visited_neighbors == 0:
            self.step_back()
            return

        # Has more neighbors, so decide the step
        # Defining next neighbor( Returning -1 should go back)
        next_neighbor_id = self.define_agent_next_step(
            non_visited_neighbors=non_visited_neighbors,
        )

        # No valid neighbor to next step
        if next_neighbor_id == "-1":
            self.step_back()
            return

        self.parent_list.append(self.current_node_id)
        self.search.append(self.current_node_id)
        self.effective_path.append(self.current_node_id)
        self.current_node_id = next_neighbor_id
        return

    def define_agent_next_step(
        self,
        non_visited_neighbors: List[str],
    ) -> str:
        # Next Step during DFS
        if self.status == AgentStatus.DFS or self.filled_interval:
            next_step = self.define_next_dfs_step(non_visited_neighbors)
            return next_step

        if self.algorithm == Algorithm.SELF and (
            self.status == AgentStatus.SEARCHING_INTERVAL
            or self.status == AgentStatus.IN_INTERVAL
        ):
            next_step = self.define_next_self_step(non_visited_neighbors)
            return next_step

    def define_next_dfs_step(
        self,
        non_visited_neighbors: List[str],
    ) -> str:
        total_number_of_neighbors = len(non_visited_neighbors)

        neighbors_backtrack = []

        # Add neighbors to tree
        for index, neighbor in enumerate(non_visited_neighbors):
            # Check if the neighbor is already in tree and is a backtrack
            node_in_tree = (
                self.known_tree.nodes.get(neighbor) is not None
                and self.known_tree.nodes.get(neighbor).get("radix") is not None
            )
            neighbor_is_backtrack = False
            if node_in_tree:
                for edges in self.known_tree.neighbors(neighbor):
                    if edges == self.current_node_id:
                        neighbor_is_backtrack = True
                        break
            neighbors_backtrack.append(neighbor_is_backtrack)
            if neighbor_is_backtrack:
                # No need to add, just update
                self.known_tree.nodes[neighbor]["status"] = "DFS-BT"
            else:
                self.known_tree = add_edge_to_graph(
                    self.current_node_id,
                    neighbor,
                    self.known_tree,
                    (
                        (str(index), str(total_number_of_neighbors))
                        if total_number_of_neighbors != 1
                        else ("X", "X")
                    ),
                    ("X", "X"),
                    "DFS",
                )

        for index, neighbor in enumerate(non_visited_neighbors):
            if neighbors_backtrack[index]:
                node_index = self.known_tree.nodes[neighbor]["index"]
                choice = (int(node_index[0]), int(node_index[1]))
                self.visited_path.append(choice)
            else:
                if total_number_of_neighbors == 1:
                    self.visited_path.append((-1, -1))
                else:
                    self.visited_path.append((index, total_number_of_neighbors))
            return neighbor

    def define_next_self_step(
        self,
        non_visited_neighbors: List[str],
    ) -> str:
        neighbors_weights = self.get_neighbors_weights(non_visited_neighbors)
        self.add_neighbors_to_tree(non_visited_neighbors, neighbors_weights)
        total_number_of_neighbors = len(non_visited_neighbors)

        # Decide next step based on interval
        for index, neighbor in enumerate(non_visited_neighbors):
            neighbor_interval = neighbors_weights[index]

            # If the current child's interval is on the right of the agent's interval, surely the agent finished its interval
            if self.interval[1] <= neighbor_interval[0]:
                self.filled_interval = True
                break

            neighbor_is_inside_agent_interval = (
                self.interval[0] < neighbor_interval[1]
                and self.interval[1] > neighbor_interval[0]
            )

            if neighbor_is_inside_agent_interval:
                neighbor_is_backtrack = neighbor_interval[2]
                if neighbor_is_backtrack:
                    node_index = self.known_tree.nodes[neighbor]["index"]
                    choice = (int(node_index[0]), int(node_index[1]))
                    self.visited_path.append(choice)
                else:
                    if total_number_of_neighbors == 1:
                        self.visited_path.append((-1, -1))
                    else:
                        self.visited_path.append((index, total_number_of_neighbors))
                return neighbor

        # If the agent is in the root and it doesn't find a node that fills the requirement, it finished its interval
        # It occurs when the agent come back to root but it has already been visited the root's children
        # In the context of this Bachelor's thesis, the agent will stop
        if self.current_node_id == self.starting_node.id:
            self.filled_interval = True

        # If didn't fill interval yet, step back
        if not self.filled_interval:
            return "-1"

        # If interval was filled, start DFS
        print(f"This agent {self.id} search failed. Trying DFS")
        self.status = AgentStatus.DFS
        return self.define_next_dfs_step(non_visited_neighbors)

    def get_neighbors_weights(
        self,
        non_visited_neighbors: List[str],
    ) -> List[Tuple[float, float, bool]]:
        current_node_interval_string = self.known_tree.nodes[self.current_node_id][
            "radix"
        ]
        current_node_interval = (
            float(current_node_interval_string[0]),
            float(current_node_interval_string[1]),
        )
        current_node_interval_size = current_node_interval[1] - current_node_interval[0]
        chunk = current_node_interval_size / len(non_visited_neighbors)
        neighbor_weights = []

        neighbor_count = 0
        for neighbor in non_visited_neighbors:
            # Check if the neighbor is already in tree and is a backtrack
            node_in_tree = (
                self.known_tree.nodes.get(neighbor) is not None
                and self.known_tree.nodes.get(neighbor).get("radix") is not None
            )
            neighbor_is_backtrack = False
            if node_in_tree:
                for edges in self.known_tree.neighbors(neighbor):
                    if edges == self.current_node_id:
                        neighbor_is_backtrack = True
                        break

            if neighbor_is_backtrack:
                neighbor_interval = self.known_tree.nodes[neighbor]["radix"]
                neighbor_interval = (
                    float(neighbor_interval[0]),
                    float(neighbor_interval[1]),
                    True,
                )
            else:
                neighbor_interval_start = (
                    current_node_interval[0] + chunk * neighbor_count
                )
                neighbor_interval_end = neighbor_interval_start + chunk
                neighbor_interval = (
                    neighbor_interval_start,
                    neighbor_interval_end,
                    False,
                )

            neighbor_weights.append(neighbor_interval)

            neighbor_count += 1

        return neighbor_weights

    def add_neighbors_to_tree(
        self,
        non_visited_neighbors: List[str],
        neighbor_weights: List[Tuple[float, float]],
    ):
        for index, neighbor in enumerate(non_visited_neighbors):
            # Check if the neighbor is already in tree and is a backtrack
            neighbor_is_backtrack = neighbor_weights[index][2]

            # If neighbor is backtrack, no need to add it to tree, just update
            if neighbor_is_backtrack:
                self.known_tree.nodes[neighbor]["status"] = "Int-BT"
            else:
                self.known_tree = add_edge_to_graph(
                    self.current_node_id,
                    neighbor,
                    self.known_tree,
                    (
                        (str(index), str(len(non_visited_neighbors)))
                        if len(non_visited_neighbors) != 1
                        else ("X", "X")
                    ),
                    neighbor_weights[index],
                    "Int",
                )
        return

    def move(self, graph: nx.Graph):
        while True:
            self.move_one_step(graph)
            if (
                self.status == AgentStatus.FINISHED
                or self.status == AgentStatus.STOPPED
            ):
                return

    def print_tree(self, title: Optional[str]):
        self.known_tree = preprocess_node_ids(self.known_tree)
        root_id_cleaned = self.starting_node.id.replace(",", " ")
        display_graph(self.known_tree, root_id_cleaned, None, True, title)
