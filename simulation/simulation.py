from typing import List, Optional

import networkx as nx

from my import MyAlgorithm
from simulation.agent import Agent, Algorithm, Color, Node
from simulation.utils import concatenate_new_elements

defaultAgentColorList = [
    Color.red,
    Color.blue,
    Color.yellow,
    Color.orange,
    Color.pink,
    Color.cyan,
    Color.black,
]


class Simulation:
    def __init__(
        self,
        algorithm: Algorithm,
        n_agents: int,
        graph: nx.Graph,
        starting_node_id: str,
    ) -> None:
        self.n_agents = n_agents
        self.algorithm = algorithm
        self.graph = graph
        self.agents: List[Agent] = []
        self.division = division = 1.0 / self.n_agents

        starting_node = self.graph.nodes[starting_node_id]
        starting_node_color = (
            starting_node.get("color") if starting_node.get("color") else "lightblue"
        )
        starting_node_finish = (
            starting_node.get("finish") if starting_node.get("finish") else False
        )
        starting_node_neighbors = list(self.graph.adj[starting_node_id])

        node = Node(
            id=starting_node_id,
            color=starting_node_color,
            finish=starting_node_finish,
            edges=[
                (starting_node_id, neighbor) for neighbor in starting_node_neighbors
            ],
        )

        for i in range(0, self.n_agents):
            start = i * division
            end = (i + 1) * division
            agentInterval = (start, end)

            self.agents.append(
                Agent(
                    id=i,
                    algorithm=self.algorithm,
                    color=defaultAgentColorList[i],
                    starting_node=node,
                    interval=agentInterval,
                )
            )

        # Metrics
        self.pionner_steps = None
        self.paths = []
        self.agent_searches = []
        self.effective_paths = []
        self.explored_paths = []
        self.goals_found = []
        self.total_steps = 0
        self.fraction_explored = 0
        self.fraction_pionner = 0

    def simulate(self, shoud_print: Optional[bool]) -> None:

        # Path for each agent
        for agent in self.agents:
            search, effective_path, explored_path, found_goal = agent.move(self.graph)

            self.paths.append({agent.id: search})
            self.agent_searches.append(search)
            self.effective_paths.append(effective_path)
            concatenate_new_elements(self.explored_paths, explored_path)
            self.goals_found.append(found_goal)

            agent_steps = len(search) - 1
            self.total_steps += agent_steps

            # Get the number of the steps of the pionner
            if found_goal == True:
                if self.pionner_steps is None:
                    self.pionner_steps = agent_steps
                elif self.pionner_steps > agent_steps:
                    self.pionner_steps = agent_steps

        # Calculate Fraction Metrics
        self.fraction_explored = len(self.explored_paths) / (
            self.graph.number_of_nodes()
        )

        # Calculate the fraction of the maze explored until the pionner find the goal
        cells = []
        for i in range(self.n_agents):
            aux = self.agent_searches[i][0 : self.pionner_steps]

            for e in aux:
                if e not in cells:
                    cells.append(e)
        self.fraction_pionner = len(cells) / (self.graph.number_of_nodes())

        # Print Result
        if shoud_print is not None and shoud_print:
            print("PRINTING MISSING")
