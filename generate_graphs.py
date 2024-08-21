# Importing necessary libraries and functions
import argparse
import os
from enum import Enum

import networkx as nx

from compare import GraphSize


class GraphType(Enum):
    RANDOM_POWER_LAW_TREE = "random_power_law_tree"


def convert_enum_to_int(graph_size: GraphSize):
    value_str = graph_size.value
    if "_" in value_str:
        # Split the string by '_by_' and multiply the two parts
        parts = value_str.split("_by_")
        return int(parts[0]) * int(parts[1])
    else:
        return int(value_str)


def generate_graphs(
    graph_type: GraphType, graph_size: GraphSize, n_graphs: int
) -> None:
    # Generate Graphs Dir
    sanity_res_dir = os.path.join(f"graphs", graph_size.value)
    os.makedirs(sanity_res_dir, exist_ok=True)

    n_nodes = convert_enum_to_int(graph_size)

    # Generate graphs

    for i in range(n_graphs):
        success = False
        while not success:
            try:
                # Attempt to generate a graph with max tries
                G = nx.random_powerlaw_tree(n=n_nodes, tries=10000, seed=None)
                success = True
            except nx.NetworkXError:
                # If tries are insufficient, loop will try again
                print(f"Retrying to generate graph {i + 1} due to insufficient tries.")
                continue
        
        # Define the file path
        file_path = os.path.join(sanity_res_dir, f"graph_{graph_size.value}__{i + 1}.graphml")
        
        # Save the graph to a graphml file
        nx.write_graphml(G, file_path)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze graphs and generate statistics."
    )
    parser.add_argument(
        "--graph_type",
        type=GraphType,
        default=GraphType.RANDOM_POWER_LAW_TREE,
        help="Generator that should be used when generating new graphs",
    )
    parser.add_argument(
        "--graph_size",
        type=GraphSize,
        default=GraphSize.N_100,
        help="Number of nodes that should make the graph",
    )
    parser.add_argument(
        "--n_graphs",
        type=int,
        default=250,
        help="Number of random graphs that should be created using a given configuration",
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    os.makedirs("graphs/", exist_ok=True)
    generate_graphs(
        args.graph_type,
        args.graph_size,
        args.n_graphs,
    )
