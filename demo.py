import argparse

from simulation.graph_utils import construct_graph, load_graph
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

    if args.graph is not None:
        graph = load_graph(10, 10, args.graph)
    else:
        graph = construct_graph(10, 10)

    simulation = Simulation(
        algorithm=args.algorithm,
        n_agents=args.agents,
        graph=graph,
    )

    result = simulation.simulate(shoud_print=True)
    print(result)
