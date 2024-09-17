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


def contract_paths(uncontracted_graph: nx.Graph, root: int) -> nx.Graph:
    # Copy graph
    contracted_graph = uncontracted_graph.copy()
    # All Degree 2 Nodes
    degree_two_nodes = [
        node
        for node, degree in contracted_graph.degree()
        if degree == 2 and node != root
    ]

    while len(degree_two_nodes) > 0:
        for v in degree_two_nodes:
            try:
                neighbors = list(contracted_graph.neighbors(v))
            except:
                # Searched already contracted node, just continue
                continue
            # Check it has only 2 neighbors
            if len(neighbors) == 2:
                u, w = neighbors
                
                # Choosing main neighbor
                # Order nodes by rule: root > node with more neighbors
                sorted_neighbors = sorted(
                    [u, w],
                    key=lambda x: (x == root, contracted_graph.degree(x)),
                    reverse=True,
                )
                main_node = sorted_neighbors[0]
                auxiliar_node = sorted_neighbors[1]
                last_node = v  # v is the node to be contracted first
                
                # Contract auxiliar and last, maintaining auxiliar
                contracted_graph = nx.contracted_nodes(
                    contracted_graph, auxiliar_node, last_node, self_loops=False, copy=False
                )
                # Remove "contraction" metadata
                if "contraction" in contracted_graph.nodes[auxiliar_node]:
                    del contracted_graph.nodes[auxiliar_node]["contraction"]
                # Contract main and aux, maintaining main
                contracted_graph = nx.contracted_nodes(
                    contracted_graph, main_node, auxiliar_node, self_loops=False, copy=False
                )
                # Remove "contraction" metadata
                if "contraction" in contracted_graph.nodes[main_node]:
                    del contracted_graph.nodes[main_node]["contraction"]
        degree_two_nodes = [
            node
            for node, degree in contracted_graph.degree()
            if degree == 2 and node != root
        ]

    return contracted_graph


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
    G = contract_paths(G, 0)

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
