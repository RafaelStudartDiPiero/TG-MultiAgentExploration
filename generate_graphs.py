# Importing necessary libraries and functions
import argparse
import os
import random
from enum import Enum

import networkx as nx

from compare import GraphSize


class GraphType(Enum):
    BALANCED_TREE = "balanced_tree"
    FULL_RARY_TREE = "full_rary_tree"
    RANDOM_UNLABELED_TREE = "random_unlabeled_tree"
    RANDOM_POWER_LAW_TREE = "random_power_law_tree"


def convert_enum_to_int(graph_size: GraphSize):
    value_str = graph_size.value
    if "_" in value_str:
        # Split the string by '_by_' and multiply the two parts
        parts = value_str.split("_by_")
        return int(parts[0]) * int(parts[1])
    else:
        return int(value_str)


def generate_graph_by_enum(graph_type: GraphType, n_nodes: int) -> nx.Graph:
    G = None

    # Generate Basic Graph
    if graph_type == GraphType.BALANCED_TREE:
        # TODO: Fix This R and H
        G = nx.balanced_tree(r=10, h=3)
    elif graph_type == GraphType.FULL_RARY_TREE:
        # TODO: Fix this R
        G = nx.full_rary_tree(r=3, n=n_nodes)
    elif graph_type == GraphType.RANDOM_POWER_LAW_TREE:
        # TODO: Fix this power law
        G = nx.random_powerlaw_tree(n=n_nodes, tries=10000, seed=None)
    elif graph_type == GraphType.RANDOM_UNLABELED_TREE:
        G = nx.random_unlabeled_tree(n_nodes, number_of_trees=None, seed=None)

    # Contract Paths

    # Set root and finish
    G.nodes[0]["color"] = "red"

    # Find all leaf nodes (nodes with degree 1)
    leaf_nodes = [node for node in G.nodes if G.degree[node] == 1]
    # # Choose a random leaf node and color it as green
    finish_node = random.choice(leaf_nodes)
    G.nodes[finish_node]["color"] = "green"
    G.nodes[finish_node]["finish"] = True

    return G


def generate_graphs(
    graph_type: GraphType, graph_size: GraphSize, n_graphs: int
) -> None:
    # Generate Type Graph Dir
    type_graph_dir = os.path.join(f"graphs", graph_type.value)
    os.makedirs(type_graph_dir, exist_ok=True)
    # Generate Size Graphs Dir
    size_dir = os.path.join(type_graph_dir, graph_size.value)
    os.makedirs(size_dir, exist_ok=True)
    # Generate

    n_nodes = convert_enum_to_int(graph_size)

    # Generate graphs

    for i in range(n_graphs):
        success = False
        while not success:
            try:
                # Attempt to generate a graph with max tries
                G = generate_graph_by_enum(graph_type, n_nodes)
                success = True
            except nx.NetworkXError:
                # If tries are insufficient, loop will try again
                print(f"Retrying to generate graph {i + 1} due to insufficient tries.")
                continue

        # Define the file path
        file_path = os.path.join(size_dir, f"graph_{graph_size.value}__{i + 1}.graphml")

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
