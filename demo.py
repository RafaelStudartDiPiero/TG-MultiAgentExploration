import argparse
import random

import gmpy2

import gmpyconfig
from simulation.graph_utils import convert_maze, load_graph, get_starting_node
from simulation.simulation import Algorithm, Simulation


def parse_arguments():
    parser = argparse.ArgumentParser(description="Graph exploration algorithm.")
    parser.add_argument(
        "--algorithm",
        type=Algorithm,
        default=Algorithm.SELF,
        help="Which algorithm should be used",
    )
    parser.add_argument(
        "--agents", type=int, default=3, help="Number of agents (default: 3)"
    )
    parser.add_argument(
        "--graph",
        type=str,
        default=None,
        help="File path to saved graph",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # Args
    args = parse_arguments()

    if args.graph.endswith(".graphml"):
        graph = load_graph(args.graph)
        starting_node_id = get_starting_node(random.choice(list(graph.nodes)))
    else:
        graph, rows, columns = convert_maze(args.graph)
        starting_node_id = f"{rows},{columns}"

    simulation = Simulation(
        algorithm=args.algorithm,
        n_agents=args.agents,
        graph=graph,
        starting_node_id=starting_node_id,
    )

    simulation.simulate(shoud_print=True, should_print_trees=False)
