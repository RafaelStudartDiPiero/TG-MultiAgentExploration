import argparse

from simulation.graph_utils import construct_graph, load_graph, convert_maze
from simulation.simulation import Simulation


def parse_arguments():
    parser = argparse.ArgumentParser(description="Graph exploration algorithm.")
    parser.add_argument(
        "--algorithm",
        type=str,
        default="self",
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
    
    graph,rows, columns = convert_maze(args.graph)

    simulation = Simulation(
        algorithm=args.algorithm,
        n_agents=args.agents,
        graph=graph,
        starting_node_id=f"{rows},{columns}",
        is_maze=True,
    )

    simulation.simulate(shoud_print=True)
