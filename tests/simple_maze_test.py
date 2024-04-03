from simulation.graph_utils import load_graph
from simulation.simulation import Algorithm, Simulation


def test_simple_maze_simulation():
    graph = load_graph(10, 10, "test1.csv")

    simulation = Simulation(
        algorithm=Algorithm.SELF.value,
        n_agents=3,
        graph=graph,
    )

    steps, pionner_steps, fraction, fraction_pionner = simulation.simulate(
        shoud_print=False
    )

    assert steps == 70
    assert pionner_steps == 16
    assert fraction - 0.722222 < 0.1
    assert fraction_pionner - 0.72222 < 0.1
