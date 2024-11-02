# Importing necessary libraries and functions
import argparse
import os
import pickle
from enum import Enum
from typing import List

import gmpy2
import matplotlib.pyplot as plt

import gmpyconfig
from simulation.simulation import Algorithm


class GraphSize(Enum):
    SIZE_10 = "10_by_10"
    SIZE_20 = "20_by_20"
    SIZE_30 = "30_by_30"
    SIZE_40 = "40_by_40"
    N_10 = "10"
    N_25 = "25"
    N_50 = "50"
    N_100 = "100"
    N_250 = "250"
    N_500 = "500"
    N_1000 = "1000"
    N_1500 = "1500"


class Metric(Enum):
    AVG_STEPS = "avg_steps"
    STD_STEPS = "std_steps"
    AVG_PIONEER_STEPS = "avg_pioneer_steps"
    STD_PIONEER_STEPS = "std_pioneer_steps"
    AVG_FRACTION = "avg_fraction"
    STD_FRACTION = "std_fraction"
    AVG_FRACTION_PIONEER = "avg_fraction_pioneer"
    STD_FRACTION_PIONEER = "std_fraction_pioneer"


def get_algorithm_label(algorithm: Algorithm) -> str:
    algorithm_labels = {
        Algorithm.SELF: "1I",
        Algorithm.TARRY: "Tarry",
        Algorithm.TWO_INTERVAL: "2I",
        Algorithm.TARRY_INTERVAL_TIE_BREAKER: "Tarry-Tie",
        Algorithm.TARRY_DELAYED_INTERVAL_TIE_BREAKER: "Tarry-Delay",
        Algorithm.TARRY_INTERVAL_PRIORITY: "Tarry-Priority",
    }
    return algorithm_labels[algorithm]


def get_metric_label(metric: Metric) -> str:
    metric_labels = {
        Metric.AVG_STEPS: "Average Steps",
        Metric.STD_STEPS: "Standard Deviation of Steps",
        Metric.AVG_PIONEER_STEPS: "Average Pioneer Steps",
        Metric.STD_PIONEER_STEPS: "Standard Deviation of Pioneer Steps",
        Metric.AVG_FRACTION: "Average Fraction Explored",
        Metric.STD_FRACTION: "Standard Deviation of Fraction Explored",
        Metric.AVG_FRACTION_PIONEER: "Fraction Explored when Pioneer arrives",
        Metric.STD_FRACTION_PIONEER: "Standard Deviation of Fraction Explored when Pioneer arrives",
    }
    return metric_labels[metric]


def compare_explorations(
    algorithms: List[Algorithm],
    base_path: str,
    graph_size: GraphSize,
    metrics: List[Metric],
    split_legend: bool,
    title: str,
    relative: bool = False,
):
    algorithm_colors = ["blue", "red", "green", "orange"]
    metric_markers = [".", "d", "s"]

    # Loading Results Correctly
    algorithms_results = []
    for algorithm in algorithms:
        with open(
            f"results/data/{base_path}/{algorithm.value}/{graph_size.value}_result.pkl",
            "rb",
        ) as f:
            results = pickle.load(f)
            algorithms_results.append(results)
    # Define Baseline
    baseline_results = algorithms_results[0] if relative else None

    # Starting Figure
    plt.figure(figsize=(10, 6))
    used_lines = []
    # Adding lines for each algorithm
    for algorithm_index, results in enumerate(algorithms_results):
        agents = [result["agents"] for result in results]
        # Creating lines for each metric
        for metric_index, metric in enumerate(metrics):
            metric_data = [result[metric.value] for result in results]
            
            if relative and baseline_results is not None:
                baseline_data = [baseline_result[metric.value] for baseline_result in baseline_results]
                metric_data = [
                    (current - baseline) / baseline if baseline != 0 else 0
                    for current, baseline in zip(metric_data, baseline_data)
                ]
            metric_label_prefix = "Relative " if relative else ""
            # Create the line plots
            (metric_line,) = plt.plot(
                agents,
                metric_data,
                label=f"{get_algorithm_label(algorithms[algorithm_index])} - {metric_label_prefix}{get_metric_label(metric)}",
                marker=metric_markers[metric_index % len(metric_markers)],
                color=algorithm_colors[algorithm_index % len(algorithm_colors)],
                linestyle="--" if metric == Metric.STD_STEPS else None,
            )
            used_lines.append(metric_line)
    # Creating Labels and Legend
    plt.xlabel("Number of Agents")
    ylabel = "Steps"
    if all("fraction" in metric.value for metric in metrics):
        ylabel = "Relative Difference of Explored Fraction" if relative else "Explored Fraction"
    else:
        ylabel = "Relative Difference of Steps" if relative else "Steps"
    plt.ylabel(ylabel=ylabel)
    plt.title(title)
    # Display the plot
    plt.grid(True)
    plt.tight_layout()
    if not split_legend:
        plt.legend()
    # Saving Plot
    algorithms_string = ""
    for index, algorithm in enumerate(algorithms):
        if index == 0:
            algorithms_string += f"{algorithm.value}_"
            continue
        algorithms_string += f"vs_{algorithm.value}_"
    metrics_string = ""
    for index, metric in enumerate(metrics):
        metrics_string += f"{metric.value}_"
    # Creating Base Directoy
    algorithms_base_path_comparison_dir = os.path.join(
        "results/plot/compare", base_path
    )
    os.makedirs(algorithms_base_path_comparison_dir, exist_ok=True)
    
    relative_suffix = "_relative" if relative else ""

    # Creating Directory
    algorithms_comparison_dir = os.path.join(
        algorithms_base_path_comparison_dir, algorithms_string
    )
    os.makedirs(algorithms_comparison_dir, exist_ok=True)

    file_path = f"results/plot/compare/{base_path}/{algorithms_string}/{metrics_string}_{graph_size.value}{relative_suffix}.svg"
    plt.savefig(file_path, format="svg")
    # Saving Legend
    if split_legend:
        fig_legend = plt.figure(figsize=(4, 2))
        legend = fig_legend.legend(handles=used_lines, loc="center", ncol=1)
        fig_legend.canvas.draw()
        # Save the legend as SVG
        legend_file_path = f"results/plot/compare/{base_path}/{algorithms_string}/{metrics_string}_{graph_size.value}_legend.svg"
        fig_legend.savefig(legend_file_path, format="svg")
    plt.close()
    return


def convert_algorithms_list(algorithms: str) -> List[Algorithm]:
    try:
        return [Algorithm[item.strip().upper()] for item in algorithms.split(",")]
    except KeyError as e:
        raise argparse.ArgumentTypeError(f"{str(e)} is not a valid Algorithm")


def convert_metrics_list(metrics: str) -> List[Metric]:
    try:
        return [Metric[item.strip().upper()] for item in metrics.split(",")]
    except KeyError as e:
        raise argparse.ArgumentTypeError(f"{str(e)} is not a valid Metric")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Compare algorithms' results.")
    parser.add_argument(
        "--algorithms",
        type=str,
        default="self,tarry",
        help="A comma-separated list of algorithms that should be compared.",
    )
    parser.add_argument(
        "--base_path",
        type=str,
        default="mazes/",
        help="Base path where result directories are located",
    )
    parser.add_argument(
        "--graph_size",
        type=GraphSize,
        default=GraphSize.SIZE_10,
        help="Specific size directory to use (e.g., '10_by_10', '20_by_20').",
    )
    parser.add_argument(
        "--metrics",
        type=str,
        default="avg_pioneer_steps",
        help="A comma-separated list of metrics that should be plotted",
    )
    parser.add_argument(
        "--split_legend",
        type=bool,
        default=False,
        help="Should generate separate legends",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Graph Exploration",
        help="Title of Generated Plot",
    )
    parser.add_argument(
        "--relative",
        type=bool,
        default=False,
        help="Relative Metrics"
    )
    args = parser.parse_args()

    # Convert comma-separated strings to lists of enums
    args.algorithms = convert_algorithms_list(args.algorithms)
    args.metrics = convert_metrics_list(args.metrics)

    return args


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    # Generate Comparation Plots
    compare_explorations(
        args.algorithms,
        args.base_path,
        args.graph_size,
        args.metrics,
        args.split_legend,
        args.title,
        args.relative,
    )
