import argparse

from simulation.graph_utils import convert_maze, load_graph
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

    if args.graph.endswith(".graphml"):
        graph = load_graph(args.graph)
        starting_node_id = "1"
        is_maze = False
    else:
        graph, rows, columns = convert_maze(args.graph)
        starting_node_id = f"{rows},{columns}"
        is_maze = True

    simulation = Simulation(
        algorithm=args.algorithm,
        n_agents=args.agents,
        graph=graph,
        starting_node_id=starting_node_id,
        is_maze=is_maze,
    )

    simulation.simulate(shoud_print=False, should_print_trees=True)
    
    print(simulation.agent_searches[2])
    print(simulation.effective_paths[2])
    print(simulation.visited_paths[2])
