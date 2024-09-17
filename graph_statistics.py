# Importing necessary libraries and functions
import argparse
import os
import pickle
from statistics import stdev, mean
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from simulation.graph_utils import convert_maze, load_graph
from simulation.graph import sort_neighbors


def custom_dfs_tree(graph, start_node):
    visited = set()
    dfs_tree = nx.Graph()

    def dfs(node):
        visited.add(node)
        neighbors = list(graph.neighbors(node))
        sorted_neighbors = sort_neighbors(neighbors, node)

        for neighbor in sorted_neighbors:
            if neighbor not in visited:
                dfs_tree.add_edge(node, neighbor)
                dfs(neighbor)

    dfs(start_node)
    return dfs_tree


def analyze_graph(graph: nx.Graph, root_id: str) -> Tuple[int, int, int]:
    # Convert Graph into Tree
    tree = custom_dfs_tree(graph, root_id)
    visited = set()

    # Calculate Depth and Leaf Nodes
    def dfs(node, parent, depth):
        # Initialize variables
        visited.add(node)
        max_depth = depth
        leaf_count = 0

        neighbors = list(tree.neighbors(node))
        valid_neighbors = [n for n in neighbors if n != parent]

        # If node is a leaf (no valid children)
        if not valid_neighbors:
            return depth, 1

        # Check the number of valid neighbors
        if len(valid_neighbors) > 1:
            depth += 1  # Increase depth if there are multiple valid neighbors

        for neighbor in neighbors:
            if neighbor not in visited:
                child_depth, child_leaf_count = dfs(neighbor, node, depth)
                max_depth = max(max_depth, child_depth)
                leaf_count += child_leaf_count

        return max_depth, leaf_count

    max_depth, leaf_count = dfs(root_id, None, 0)
    return max_depth, leaf_count, len(graph.nodes)


def analyze_directory(graph_dir: str) -> Tuple[float, float, float]:
    depths = []
    leaf_counts = []
    node_counts = []

    for file_name in os.listdir(graph_dir):
        file_path = os.path.join(graph_dir, file_name)

        if file_path.endswith(".graphml"):
            graph = load_graph(file_path)
            starting_node_id = "0"
        else:
            graph, rows, columns = convert_maze(file_path)
            starting_node_id = f"{rows},{columns}"

        # Analyze the current graph
        max_depth, leaf_nodes, n_nodes = analyze_graph(graph, starting_node_id)
        depths.append(max_depth)
        leaf_counts.append(leaf_nodes)
        node_counts.append(n_nodes)

    # Calculate the mean of the depths and leaf counts
    mean_depth = mean(depths)
    mean_leaf_count = mean(leaf_counts)
    mean_n_nodes = mean(node_counts)
    # Number of Graphs
    print(f"Number of Graphs:{len(depths)}")

    # Save Data
    sanity_res_dir = os.path.join(f"sanity_checks", graph_dir)
    os.makedirs(sanity_res_dir, exist_ok=True)
    with open(os.path.join(sanity_res_dir, f"result.pkl"), "wb") as f:
        pickle.dump({"depth": mean_depth, "leaf_count": mean_leaf_count, "n_nodes": mean_n_nodes}, f)

    return mean_depth, mean_leaf_count, mean_n_nodes


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze graphs and generate statistics."
    )
    parser.add_argument(
        "--graph-path",
        type=str,
        default=None,
        help="File path to saved graph(file) or saved graphs(directory)",
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    if os.path.isdir(args.graph_path):
        mean_depth, mean_leaf_count, mean_n_nodes = analyze_directory(args.graph_path)
        print(f"Mean Depth: {mean_depth}")
        print(f"Mean Leaf Nodes: {mean_leaf_count}")
        print(f"Mean Nodes: {mean_n_nodes}")
    else:
        if args.graph_path.endswith(".graphml"):
            graph = load_graph(args.graph_path)
            starting_node_id = "0"
        else:
            graph, rows, columns = convert_maze(args.graph_path)
            starting_node_id = f"{rows},{columns}"

        # Analyze single graph
        max_depth, leaf_nodes, n_nodes = analyze_graph(graph, starting_node_id)
        print(f"Depth: {max_depth}")
        print(f"Leaf Nodes: {leaf_nodes}")
        print(f"Nodes: {n_nodes}")
