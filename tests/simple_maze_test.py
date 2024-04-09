from simulation.graph_utils import convert_maze
from simulation.simulation import Algorithm, Simulation


def test_simple_maze_simulation():
    graph, rows, columns = convert_maze("test1.csv")

    simulation = Simulation(
        algorithm=Algorithm.SELF.value,
        n_agents=3,
        graph=graph,
        starting_node_id=f"{rows},{columns}",
    )

    simulation.simulate(shoud_print=False)

    assert simulation.total_steps == 70
    assert simulation.pionner_steps == 16
    assert simulation.fraction_explored - 0.722222 < 0.1
    assert simulation.fraction_pionner - 0.72222 < 0.1
