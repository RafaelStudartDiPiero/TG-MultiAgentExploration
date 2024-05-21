from typing import List, Optional

import matplotlib.pyplot as plt
import networkx as nx

from simulation.agent import Agent, Algorithm, Color, Node
from simulation.graph_utils import display_graph, display_maze
from simulation.utils import concatenate_new_elements

defaultAgentColorList = [
    Color.red,
    Color.blue,
    Color.cyan,
    Color.pink,
    Color.orange,
    Color.yellow,
    Color.black,
]


class Simulation:
    def __init__(
        self,
        algorithm: Algorithm,
        n_agents: int,
        graph: nx.Graph,
        starting_node_id: str,
        is_maze: Optional[bool] = False,
    ) -> None:
        self.n_agents = n_agents
        self.algorithm = algorithm
        self.graph = graph
        self.is_maze = is_maze if is_maze is not None else False
        self.agents: List[Agent] = []
        self.division = division = 1.0 / self.n_agents if self.n_agents > 0 else 0
        self.starting_node_id = starting_node_id

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
                    color=defaultAgentColorList[i % len(defaultAgentColorList)],
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
        self.visited_paths = []
        self.total_steps = 0
        self.fraction_explored = 0
        self.fraction_pionner = 0

    def simulate(
        self, shoud_print: Optional[bool], should_print_trees: Optional[bool]
    ) -> None:
        
        if self.n_agents == 0:
            return

        # Path for each agent
        for agent in self.agents:
            agent.move(self.graph)

            search = agent.search
            effective_path = agent.effective_path
            explored_path = agent.explored
            found_goal = agent.finished
            visited_path = agent.visited_path

            self.paths.append({agent.id: search})

            self.agent_searches.append(search)
            self.effective_paths.append(effective_path)
            concatenate_new_elements(self.explored_paths, explored_path)
            self.goals_found.append(found_goal)
            self.visited_paths.append(visited_path)

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
            plt.ion()
            fig, ax = plt.subplots()
            if self.is_maze:
                display_maze(self.graph, 6, 6, ax=ax)
            else:
                display_graph(self.graph, self.starting_node_id)

            # Initialize dictionary to keep track of current step for each agent
            agent_step_indices = {agent.id: 0 for agent in self.agents}
            remaining_agents = [
                agent for agent in self.agents
            ]  # List of agent IDs with remaining steps
            current_agent_index = 0

            # Function to check if any agent has remaining steps
            def any_remaining_steps():
                return any(
                    agent_step_indices[agent.id]
                    < len(self.paths[agent.id][agent.id]) - 1
                    for agent in remaining_agents
                )

            # Loop until all agents have completed their steps
            while any_remaining_steps():
                # Wait for key press before moving the next agent
                input("Press Enter to move the next agent...")

                # Move the next available agent
                agent = remaining_agents[current_agent_index]
                if (
                    agent_step_indices[agent.id]
                    < len(self.paths[agent.id][agent.id]) - 1
                ):
                    agent_step_indices[agent.id] += 1
                    # Print the current step for the agent
                    step_node = self.paths[agent.id][agent.id][
                        agent_step_indices[agent.id]
                    ]
                    previous_step_node = self.paths[agent.id][agent.id][
                        agent_step_indices[agent.id] - 1
                    ]
                    print(
                        f"Agent {agent.id} step {agent_step_indices[agent.id]}: {step_node}"
                    )
                    self.graph.nodes[step_node]["color"] = agent.color.value[0]
                    self.graph.nodes[previous_step_node]["color"] = agent.color.value[1]
                    if self.is_maze:
                        display_maze(self.graph, 6, 6, ax=ax)
                        plt.pause(0.1)
                    else:
                        display_graph(self.graph, self.starting_node_id, ax=ax)
                        plt.pause(0.1)
                else:
                    remaining_agents.remove(
                        agent
                    )  # Remove agent ID if it has completed its steps

                if (
                    agent_step_indices[agent.id]
                    == len(self.paths[agent.id][agent.id]) - 1
                ):
                    remaining_agents.remove(
                        agent
                    )  # Remove agent ID if it has completed its steps

                if len(remaining_agents) == 0:
                    break
                current_agent_index = (current_agent_index + 1) % len(remaining_agents)

            # Simulation complete
            print("Simulation complete.")

        # Print Tree
        if should_print_trees is not None and should_print_trees:
            for agent in self.agents:
                agent.print_tree(
                    title=f"Agent ({agent.interval[0]:.3f},{agent.interval[1]:.3f})"
                )
