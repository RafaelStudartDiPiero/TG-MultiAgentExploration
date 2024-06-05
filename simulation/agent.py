from enum import Enum
from random import randint
from typing import List, Optional, Tuple

import networkx as nx

from simulation.graph import Node, sort_neighbors
from simulation.graph_utils import display_graph, preprocess_node_ids, add_edge_to_graph


class Algorithm(Enum):
    SELF = "self"
    TWO_INTERVAL = "two_interval"
    TARRY = "tarry"


class AgentStatus(Enum):
    STARTED = "STARTING"
    SEARCHING_INTERVAL = "SEARCHING_INTERVAL"
    IN_INTERVAL = "IN_INTERVAL"
    SECOND_INTERVAL_SEARCHING = "SECOND_INTERVAL_SEARCHING"
    IN_SECOND_INTERVAL = "IN_SECOND_INTERVAL"
    DFS = "DFS"
    FINISHED = "FINISHED"
    STOPPED = "STOPPED"
    TERRY_FIRST_PHASE = "TERRY_FIRST_PHASE"
    TERRY_SECOND_PHASE = "TERRY_SECOND_PHASE"
    TERRY_FOLLOW_pioneer = "TERRY_FOLLOW_pioneer"


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
        # Backup Interval defines the interval used for the two interval algorithm
        chunk = self.interval[1] - self.interval[0]
        self.backup_interval = (
            (0, chunk)
            if self.interval[1] == 1
            else (self.interval[1], self.interval[1] + chunk)
        )
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
        # The visited nodes
        self.visited = []
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
        # Check if the agent has filled it's backup interval in TWO Interval
        self.filled_backup_interval = False
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
            ) and self.algorithm != Algorithm.TWO_INTERVAL:
                # print(f"This agent {self.id} search failed. Trying DFS")
                self.status = AgentStatus.DFS
                return
            if (
                self.status == AgentStatus.SEARCHING_INTERVAL
                or self.status == AgentStatus.IN_INTERVAL
            ) and self.algorithm == Algorithm.TWO_INTERVAL:
                self.status = AgentStatus.SECOND_INTERVAL_SEARCHING
                return
            if (
                self.status == AgentStatus.IN_SECOND_INTERVAL
                or self.status == AgentStatus.SECOND_INTERVAL_SEARCHING
            ) and self.algorithm == Algorithm.TWO_INTERVAL:
                self.status = AgentStatus.DFS
                return
            if self.status == AgentStatus.DFS:
                # print(f"Agent {self.id} DFS failed, stopping.")
                self.status = AgentStatus.STOPPED
                return

        # If not root, just go back
        self.current_node_id = self.parent_list.pop()
        self.effective_path.pop()
        self.visited_path.pop()
        return

    def move_one_step(
        self,
        graph: nx.Graph,
        pioneer: Optional[int],
        pioneer_effective_path: Optional[List[str]],
        lcl: Optional[List[List[str]]],
    ):
        if self.status == AgentStatus.STARTED:
            if self.algorithm == Algorithm.TARRY:
                self.status = AgentStatus.TERRY_FIRST_PHASE
            else:
                self.status = AgentStatus.SEARCHING_INTERVAL

        if self.status == AgentStatus.FINISHED:
            # print(f"Agent {self.id} has already finished")
            return

        if self.status == AgentStatus.STOPPED:
            # print(f"Agent {self.id} stopped before finishing")
            return

        # Check the data of the current node and add it to the known graph
        node_data = graph.nodes[self.current_node_id]
        graph.nodes[self.current_node_id]["visited"] = True
        self.known_tree.nodes[self.current_node_id]["visited"] = True
        self.known_tree.nodes[self.current_node_id]["color"] = self.color.value[1]

        if self.current_node_id not in self.visited:
            self.visited.append(self.current_node_id)

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
        if count_non_visited_neighbors == 0 and (
            self.algorithm != Algorithm.TARRY
            and self.status != AgentStatus.TERRY_FOLLOW_pioneer
        ):
            graph.nodes[self.current_node_id]["deadEnd"] = True
            self.step_back()
            return

        # Has more neighbors, so decide the step
        # Defining next neighbor( Returning -1 should go back)
        next_neighbor_id = self.define_agent_next_step(
            non_visited_neighbors=non_visited_neighbors,
            graph=graph,
            pioneer=pioneer,
            pioneer_effective_path=pioneer_effective_path,
            lcl=lcl,
        )

        # No valid neighbor to next step
        if next_neighbor_id == "-1":
            graph.nodes[self.current_node_id]["deadEnd"] = True
            self.step_back()
            return

        self.parent_list.append(self.current_node_id)
        self.search.append(self.current_node_id)
        self.effective_path.append(self.current_node_id)
        self.current_node_id = next_neighbor_id

        # Checking if the next step is the finish
        graph.nodes[self.current_node_id]["visited"] = True
        node_data = graph.nodes[self.current_node_id]
        if node_data.get("finish"):
            # If the current node is the finish, end the search
            self.search.append(self.current_node_id)
            self.effective_path.append(self.current_node_id)
            self.finished = True
            self.status = AgentStatus.FINISHED
            return
        return

    def define_agent_next_step(
        self,
        non_visited_neighbors: List[str],
        graph: nx.Graph,
        pioneer: Optional[int],
        pioneer_effective_path: Optional[List[str]],
        lcl: Optional[List[List[str]]],
    ) -> str:
        # Next Step during DFS
        if (
            self.status == AgentStatus.DFS
            or (self.filled_interval and self.algorithm == Algorithm.SELF)
            or (
                self.filled_interval
                and self.filled_backup_interval
                and self.algorithm == Algorithm.TWO_INTERVAL
            )
        ):
            next_step = self.define_next_dfs_step(non_visited_neighbors)
            return next_step

        if self.status == AgentStatus.TERRY_SECOND_PHASE or (
            pioneer is not None and self.algorithm == Algorithm.TARRY
        ):
            next_step = self.define_next_second_phase_terry_step(
                non_visited_neighbors=non_visited_neighbors,
                graph=graph,
                pioneer=pioneer,
                pioneer_effective_path=pioneer_effective_path,
                lcl=lcl,
            )
            return next_step

        if self.algorithm == Algorithm.SELF and (
            self.status == AgentStatus.SEARCHING_INTERVAL
            or self.status == AgentStatus.IN_INTERVAL
        ):
            next_step = self.define_next_self_step(non_visited_neighbors)
            return next_step

        if self.algorithm == Algorithm.TWO_INTERVAL and (
            self.status == AgentStatus.SEARCHING_INTERVAL
            or self.status == AgentStatus.IN_INTERVAL
            or self.status == AgentStatus.SECOND_INTERVAL_SEARCHING
            or self.status == AgentStatus.IN_SECOND_INTERVAL
        ):
            next_step = self.define_next_two_interval_step(non_visited_neighbors)
            return next_step

        if self.algorithm == Algorithm.TARRY and (
            self.status == AgentStatus.TERRY_FIRST_PHASE
        ):
            next_step = self.define_next_first_phase_terry_step(
                non_visited_neighbors, graph
            )
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
        # print(f"This agent {self.id} search failed. Trying DFS")
        self.status = AgentStatus.DFS
        return self.define_next_dfs_step(non_visited_neighbors)

    def define_next_two_interval_step(
        self,
        non_visited_neighbors: List[str],
    ) -> str:
        neighbors_weights = self.get_neighbors_weights(non_visited_neighbors)
        self.add_neighbors_to_tree(non_visited_neighbors, neighbors_weights)
        total_number_of_neighbors = len(non_visited_neighbors)

        if not self.filled_interval:
            # Decide next step based on interval
            for index, neighbor in enumerate(non_visited_neighbors):
                neighbor_interval = neighbors_weights[index]

                # If the current child's interval is on the right of the agent's interval, surely the agent finished its interval
                if self.interval[1] <= neighbor_interval[0]:

                    self.filled_interval = True
                    self.status = AgentStatus.SECOND_INTERVAL_SEARCHING
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
            # In the context of this Bachelor's thesis, the agent will start a second interval
            if self.current_node_id == self.starting_node.id:
                self.filled_interval = True
                self.status = AgentStatus.SECOND_INTERVAL_SEARCHING

            # If didn't fill interval yet, step back
            if not self.filled_interval:
                return "-1"

        # Searching Start of Next Interval
        if (
            self.filled_interval
            and self.status == AgentStatus.SECOND_INTERVAL_SEARCHING
        ):
            # The last agent should start the second interval in the root
            if self.interval[1] == 1 and self.current_node_id != self.starting_node.id:
                return "-1"

            # Decide next step based on backup interval
            for index, neighbor in enumerate(non_visited_neighbors):
                neighbor_interval = neighbors_weights[index]
                if self.backup_interval[1] <= neighbor_interval[1]:
                    self.status = AgentStatus.IN_SECOND_INTERVAL
                    break

            # If didn't find start of new interval, step back
            if self.status == AgentStatus.SECOND_INTERVAL_SEARCHING:
                return "-1"

        # In backup interval
        if (
            not self.filled_backup_interval
            and self.status == AgentStatus.IN_SECOND_INTERVAL
        ):
            non_visited_neighbors.reverse()
            neighbors_weights.reverse()
            # Decide next step based on backup interval
            for index, neighbor in enumerate(non_visited_neighbors):
                neighbor_interval = neighbors_weights[index]

                # If the current child's interval is on the left of the agent's interval, surely the agent finished its interval
                if self.backup_interval[0] >= neighbor_interval[1]:
                    self.filled_backup_interval = True
                    break

                neighbor_is_inside_agent_interval = (
                    self.backup_interval[0] < neighbor_interval[1]
                    and self.backup_interval[1] > neighbor_interval[0]
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

            # If the agent is in the root and it doesn't find a node that fills the requirement, it finished its backup interval
            # It occurs when the agent come back to root but it has already been visited the root's children
            # In the context of this Bachelor's thesis, the agent will start a DFS
            if self.current_node_id == self.starting_node.id:
                self.filled_backup_interval = True

            # If didn't fill the backup interval yet, step back
            if not self.filled_backup_interval:
                return "-1"

        # If interval and backup were filled, start DFS
        # print(f"This agent {self.id} search failed. Trying DFS")
        self.status = AgentStatus.DFS
        return self.define_next_dfs_step(non_visited_neighbors)

    def define_next_first_phase_terry_step(
        self,
        non_visited_neighbors: List[str],
        graph: nx.Graph,
    ) -> str:
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
            if neighbor_is_backtrack:
                # No need to add, just update
                self.known_tree.nodes[neighbor]["status"] = "TARRY-PH1-BT"
            else:
                self.known_tree = add_edge_to_graph(
                    self.current_node_id,
                    neighbor,
                    self.known_tree,
                    ("X", "X"),
                    ("X", "X"),
                    "TARRY-PH1",
                )

        new_neighbors = []
        already_visited_neighbors = []

        for neighbor in non_visited_neighbors:
            if graph.nodes.get(neighbor) is not None:
                if graph.nodes.get(neighbor).get("deadEnd") != True:
                    if graph.nodes.get(neighbor).get("visited"):
                        already_visited_neighbors.append(neighbor)
                    else:
                        new_neighbors.append(neighbor)

        if len(new_neighbors) > 0:
            self.visited_path.append((-1, -1))
            if len(new_neighbors) == 1:
                return new_neighbors[0]
            return new_neighbors[randint(0, len(new_neighbors) - 1)]
        elif len(already_visited_neighbors) > 0:
            self.visited_path.append((-1, -1))
            if len(already_visited_neighbors) == 1:
                return already_visited_neighbors[0]
            return already_visited_neighbors[
                randint(0, len(already_visited_neighbors) - 1)
            ]
        else:
            return "-1"

    def define_next_second_phase_terry_step(
        self,
        non_visited_neighbors: List[str],
        graph: nx.Graph,
        pioneer: Optional[int],
        pioneer_effective_path: Optional[List[str]],
        lcl: Optional[List[List[str]]],
    ) -> str:
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
            if neighbor_is_backtrack:
                # No need to add, just update
                self.known_tree.nodes[neighbor]["status"] = "TARRY-PH1-BT"
            else:
                self.known_tree = add_edge_to_graph(
                    self.current_node_id,
                    neighbor,
                    self.known_tree,
                    ("X", "X"),
                    ("X", "X"),
                    "TARRY-PH1",
                )

        if self.status == AgentStatus.TERRY_FIRST_PHASE:
            self.status = AgentStatus.TERRY_SECOND_PHASE

        if self.status == AgentStatus.TERRY_SECOND_PHASE:
            if self.current_node_id != lcl[pioneer][self.id]:
                return "-1"
            else:
                self.status = AgentStatus.TERRY_FOLLOW_pioneer

        current_node_index = pioneer_effective_path.index(self.current_node_id)
        self.visited_path.append((-1, -1))
        return pioneer_effective_path[current_node_index + 1]

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
