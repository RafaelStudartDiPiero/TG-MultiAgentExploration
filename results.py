# Importing necessary libraries and functions
import argparse
import os
import pickle
from statistics import stdev

import matplotlib.pyplot as plt
import numpy as np

from simulation.graph_utils import convert_maze, load_graph
from simulation.simulation import Algorithm, Simulation


def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulate Graph Exploration.")
    parser.add_argument(
        "--algorithm",
        type=Algorithm,
        default=None,
        help="Which algorithm should be used",
    )
    parser.add_argument(
        "--base_path",
        type=str,
        default="mazes/",
        help="Base path where graphs directories are located",
    )
    parser.add_argument(
        "--graph_size_path",
        type=str,
        default=None,
        help="Specific size directory to use (e.g., '10_by_10', '20_by_20'). If not provided, all sizes found will be used",
    )
    parser.add_argument(
        "--max_agents",
        type=int,
        default=40,
        help="Maximum number of agents to simulate",
    )
    parser.add_argument(
        "--plot",
        type=bool,
        default=False,
        help="Should generate plots alongside results",
    )
    return parser.parse_args()


def calculate_stats(data):
    if len(data) > 1:
        try:
            avg = np.mean(data)
        except:
            avg = 0
        try:
            std_dev = stdev(data)
        except:
            std_dev = 0  # Handle cases where stdev can't be computed
    else:
        avg = 0
        std_dev = 0
    return avg, std_dev


def simulate_graph_exploration(algorithm, base_path, graph_size_path, max_agents, plot):
    if graph_size_path is None:
        # If graph_size_path is not provided, get all subdirectories in base_path
        graph_sizes = [
            name
            for name in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, name))
        ]
    else:
        graph_sizes = [graph_size_path]

    if algorithm is None:
        # If algorithm is not provided, do the simulation for all algorithms
        algorithms = list(Algorithm)
    else:
        algorithms = [algorithm]

    general_results = []

    for chosen_algorithm in algorithms:
        print(f"New Algorithm: {chosen_algorithm.value}\n")
        for graph_size in graph_sizes:
            print(f"New Graph Size:{graph_size}\n")
            graphs_path = os.path.join(base_path, graph_size)
            results = []

            for agents in range(1, max_agents + 1):
                print(f"Agents:{agents}\n")
                count = 0
                agent_steps = []
                agent_pioneer_steps = []
                fraction_explored = []
                fraction_pioneer_explored = []

                for root, dirs, files in os.walk(graphs_path):
                    for file in files:
                        graph_path = os.path.join(root, file)
                        if graph_path.endswith(".graphml"):
                            graph = load_graph(graph_path)
                            starting_node_id = "1"
                            is_maze = False
                        else:
                            graph, rows, columns = convert_maze(graph_path)
                            starting_node_id = f"{rows},{columns}"
                            is_maze = True

                        simulation = Simulation(
                            algorithm=chosen_algorithm,
                            n_agents=agents,
                            graph=graph,
                            starting_node_id=starting_node_id,
                            is_maze=is_maze,
                        )

                        simulation.simulate(False, False)
                        agent_steps.append(
                            simulation.total_steps / agents if agents > 0 else 0
                        )
                        agent_pioneer_steps.append(simulation.pioneer_steps)
                        fraction_explored.append(simulation.fraction_explored * 100)
                        fraction_pioneer_explored.append(
                            simulation.fraction_pioneer * 100
                        )
                        count += 1

                # Calculate average and standard deviation for steps and pioneer steps
                avg_steps, std_steps = calculate_stats(agent_steps)
                avg_pioneer_steps, std_pioneer_steps = calculate_stats(
                    agent_pioneer_steps
                )
                avg_fraction, std_fraction = calculate_stats(fraction_explored)
                avg_fraction_pioneer, std_fraction_pioneer = calculate_stats(
                    fraction_pioneer_explored
                )

                # Append the results to the results list
                results.append(
                    {
                        "agents": agents,
                        "avg_steps": avg_steps,
                        "std_steps": std_steps,
                        "avg_pioneer_steps": avg_pioneer_steps,
                        "std_pioneer_steps": std_pioneer_steps,
                        "avg_fraction": avg_fraction,
                        "std_fraction": std_fraction,
                        "avg_fraction_pioneer": avg_fraction_pioneer,
                        "std_fraction_pioneer": std_fraction_pioneer,
                    }
                )
            # Loading results for each graph_size into a pickle that can be found later
            general_results.append(results)

            # Define the algorithm-specific directory
            algorithm_data_dir = os.path.join("results/data", chosen_algorithm.value)
            os.makedirs(algorithm_data_dir, exist_ok=True)
            with open(
                os.path.join(algorithm_data_dir, f"{graph_size}_result.pkl"), "wb"
            ) as f:
                pickle.dump(results, f)

            # Generating and saving plots
            if plot:
                # Define the algorithm-specific directory
                algorithm_plot_dir = os.path.join(
                    "results/plot", chosen_algorithm.value
                )
                os.makedirs(algorithm_plot_dir, exist_ok=True)

                agents = [result["agents"] for result in results]
                avg_steps = [result["avg_steps"] for result in results]
                std_steps = [result["std_steps"] for result in results]
                avg_pioneer_steps = [result["avg_pioneer_steps"] for result in results]
                # Create the line plots
                plt.figure(figsize=(10, 6))
                # Plotting average steps
                plt.plot(
                    agents, avg_steps, label="Average Steps", marker=".", color="blue"
                )
                # Plotting average pioneer steps
                plt.plot(
                    agents,
                    avg_pioneer_steps,
                    label="Average Pioneer Steps",
                    marker="o",
                    color="green",
                )
                # Plotting standard deviation of steps
                plt.plot(
                    agents,
                    std_steps,
                    label="Standard Deviation - Average Steps",
                    linestyle="--",
                    marker="s",
                    color="red",
                )
                # Adding labels and legend
                plt.xlabel("Number of Agents")
                plt.ylabel("Steps")
                plt.title(
                    "Average Steps, Standard Deviation, and Pioneer Steps vs. Number of Agents"
                )
                plt.legend()
                # Display the plot
                plt.grid(True)
                plt.tight_layout()
                # Saving Plot
                file_path = os.path.join(
                    algorithm_plot_dir,
                    f"steps_std_pioneer_vs_agents_{graph_size}.svg",
                )
                plt.savefig(file_path, format="svg")
                # Close the plot to free up memory
                plt.close()

                # Graph Fraction

                # Extract data from 'results' list
                agents = [result["agents"] for result in results]
                avg_fraction = [result["avg_fraction"] for result in results]
                avg_fraction_pioneer = [
                    result["avg_fraction_pioneer"] for result in results
                ]
                # Create the line plots
                plt.figure(figsize=(10, 6))
                # Plotting average fraction
                plt.plot(
                    agents,
                    avg_fraction,
                    label="Fraction of Graph Explored",
                    marker=".",
                    color="blue",
                )
                # Plotting average fraction
                plt.plot(
                    agents,
                    avg_fraction_pioneer,
                    label="Fraction of Graph Explored when pioneer arrives",
                    linestyle="--",
                    marker="o",
                    color="green",
                )
                # Adding labels and legend
                plt.xlabel("Number of Agents")
                plt.ylabel("Fraction of Graph Explored(%)")
                plt.title("Graph Explored Fraction vs. Number of Agents")
                plt.legend()
                # Display the plot
                plt.grid(True)
                plt.tight_layout()
                # Save the plot as SVG
                file_path = os.path.join(
                    algorithm_plot_dir,
                    f"fraction_vs_agents_{graph_size}.svg",
                )
                plt.savefig(file_path, format="svg")
                # Close the plot to free up memory
                plt.close()

    return results


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    # Creating results folder if it doesn't exist
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    # Creating data results folder if it doesn't exist
    data_dir = "results/data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    # Creating plot results folder if it doesn't exist
    plot_dir = "results/plot"
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    # Run simulation
    results = simulate_graph_exploration(
        args.algorithm,
        args.base_path,
        args.graph_size_path,
        args.max_agents,
        args.plot,
    )
