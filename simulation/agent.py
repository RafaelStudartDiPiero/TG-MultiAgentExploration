from enum import Enum
from typing import List, Optional, Tuple

import networkx as nx

from simulation.graph import Node, sort_neighbors
from simulation.graph_utils import display_graph, preprocess_node_ids, add_edge_to_graph


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

        # Algorithm Attributes
        # Tree the represeting the agent path and decisions
        self.known_tree = nx.Graph()
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
        self.parent_list = []
        # The current node id
        self.current_node_id = None
        # Check if the agent has already filled it's interval
        self.filled_interval = False
        # Status of the agent search
        self.status = "LOOKING_START"

        # Start Graph
        self.starting_node = starting_node
        starting_node_id, _ = starting_node.node_view()
        self.known_tree.add_node(starting_node_id)

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
        self.parent_list = []

        # Starting parent with invalid nodes
        self.parent_list.append("-1,-1")

        while True:
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
                break

            # Fetching neighbors that weren't explored and the parent of the node
            non_visited_neighbors = sort_neighbors(
                [
                    neighbor
                    for neighbor in graph.neighbors(self.current_node_id)
                    if neighbor not in self.explored
                    and neighbor != self.parent_list[-1]
                ],
                self.current_node_id,
            )
            count_non_visited_neighbors = len(non_visited_neighbors)

            # Fetching all neighbors that weren't explored, are not the parent of the node
            # and are not in the known graph as visited(If would generate a loop)
            all_neighbors = sort_neighbors(
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

            # No more neighbors to visit, go back
            if count_non_visited_neighbors == 0:
                # Consider current cell explored
                if self.current_node_id not in self.explored:
                    self.explored.append(self.current_node_id)

                self.search.append(self.current_node_id)

                # After searching everybody and going back to root, stop
                if self.current_node_id == self.starting_node.id:
                    break

                self.current_node_id = self.parent_list.pop()
                self.effective_path.pop()
                self.visited_path.pop()

                continue

            # Defining next neighbor( Returning -1 should go back)
            next_neighbor_id = self.define_agent_next_step(
                all_neighbors=all_neighbors,
                non_visited_neighbors=non_visited_neighbors,
            )

            # No valid neighbor to next step
            if next_neighbor_id == "-1":
                # Consider current cell explored
                if self.current_node_id not in self.explored:
                    self.explored.append(self.current_node_id)

                self.search.append(self.current_node_id)

                # If not in root, just go back a step
                if self.current_node_id != self.starting_node.id:
                    self.current_node_id = self.parent_list.pop()
                    self.effective_path.pop()
                    self.visited_path.pop()
                continue

            if self.current_node_id not in self.explored:
                self.explored.append(self.current_node_id)

            self.parent_list.append(self.current_node_id)
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

        # If there is only one children, go for it
        if total_number_of_neighbors == 1:
            # If there is only one children, but it's already on tree
            # This can be a result of backtrack, check if in the interval before moving
            if (
                self.known_tree.nodes.get(all_neighbors[0]) is not None
                and self.known_tree.nodes.get(all_neighbors[0]).get("radix") is not None
                and self.parent_list[-1] != "-1,-1"
            ):
                # Checking if backtrack node is valid
                node_interval = self.known_tree.nodes[all_neighbors[0]]["radix"]
                node_interval = (float(node_interval[0]), float(node_interval[1]))
                single_node_is_inside_agent_interval = (
                    self.interval[0] < node_interval[1]
                    and self.interval[1] > node_interval[0]
                )
                if single_node_is_inside_agent_interval:
                    # Checking if backtrack or new path
                    backtrack = False
                    for edges in self.known_tree.neighbors(all_neighbors[0]):
                        if edges == self.current_node_id:
                            backtrack = True
                            break

                    if backtrack:
                        if self.id == 0:
                            print("backtrack")
                            print(self.current_node_id)
                            print(all_neighbors[0])
                        # If backtrack, maintain radix, index and path, just move
                        node_index = self.known_tree.nodes[all_neighbors[0]]["index"]
                        choice = (int(node_index[0]), int(node_index[1]))
                        self.visited_path.append(choice)
                        return all_neighbors[0]

                    # If new path, add new info
                    self.visited_path.append((-1, -1))
                    radix_current = self.known_tree.nodes[self.current_node_id].get(
                        "radix"
                    )
                    self.known_tree = add_edge_to_graph(
                        self.current_node_id,
                        all_neighbors[0],
                        self.known_tree,
                        ("X", "X"),
                        radix_current,
                    )
                    return all_neighbors[0]
                return "-1"

            # Appending no choice made
            self.visited_path.append((-1, -1))
            # Adding Radix and Index to Known Graph
            radix_current = self.known_tree.nodes[self.current_node_id].get("radix")
            self.known_tree = add_edge_to_graph(
                self.current_node_id,
                all_neighbors[0],
                self.known_tree,
                ("X", "X"),
                radix_current,
            )
            return all_neighbors[0]

        # Calculating Weight Intervals for Each Children
        relative_node_weights = self.get_relative_node_weights(
            total_number_of_neighbors
        )

        # Adding new edges to known graph
        for index, neighbor in enumerate(all_neighbors):
            self.known_tree = add_edge_to_graph(
                self.current_node_id,
                neighbor,
                self.known_tree,
                (str(index), str(total_number_of_neighbors)),
                (
                    str(relative_node_weights[index][0]),
                    str(relative_node_weights[index][1]),
                ),
            )

        # If your interval isn't filled, use logic
        if self.filled_interval == False:
            # Each each children for condition
            for i in range(total_number_of_neighbors):

                # If the current child's interval is on the right of the agent's interval, surely the agent finished its interval
                if self.interval[1] <= relative_node_weights[i][0]:
                    self.filled_interval = True
                    break

                # Checking if node interval is contained in agent interval
                node_is_inside_agent_interval = (
                    self.interval[0] < relative_node_weights[i][1]
                    and self.interval[1] > relative_node_weights[i][0]
                )

                non_visited_node = all_neighbors[i] in non_visited_neighbors

                # Go to the first node that satisfies the condition
                if node_is_inside_agent_interval and non_visited_node:
                    self.visited_path.append((i, total_number_of_neighbors))
                    return all_neighbors[i]

            # If the agent is in the root and it doesn't find a node that fills the requirement, it finished its interval
            # It occurs when the agent come back to root but it has already been visited the root's children
            # In the context of this Bachelor's thesis, the agent will stop
            if self.current_node_id == self.starting_node.id:
                self.filled_interval = True

            # If the agent doesn't finish its interval and no node that fills the requirement was found, it goes to parent
            if self.filled_interval == False:
                return "-1"

        # The agent surely finished its interval, and it will do a dummy DFS
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

    def print_tree(self):
        self.known_tree = preprocess_node_ids(self.known_tree)
        root_id_cleaned = self.starting_node.id.replace(",", " ")
        display_graph(self.known_tree, root_id_cleaned, None, True)
