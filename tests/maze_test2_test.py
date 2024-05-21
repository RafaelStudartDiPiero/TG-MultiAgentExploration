from simulation.graph_utils import convert_maze
from simulation.simulation import Algorithm, Simulation


def test_simple_maze2_simulation():
    graph, rows, columns = convert_maze("test2.csv")

    simulation = Simulation(
        algorithm=Algorithm.SELF,
        n_agents=3,
        graph=graph,
        starting_node_id=f"{rows},{columns}",
    )

    simulation.simulate(shoud_print=False, should_print_trees=False)

    # # Metrics Test
    assert simulation.total_steps == 69
    assert simulation.pionner_steps == 26
    assert simulation.fraction_explored - 0.83333 < 0.0001
    assert simulation.fraction_pionner - 0.8611111 < 0.0001

    # # Path Test - Agent 1
    assert simulation.agent_searches[0] == [
        "6,6",
        "6,5",
        "6,4",
        "6,3",
        "5,3",
        "5,4",
        "5,5",
        "4,5",
        "5,5",
        "5,6",
        "4,6",
        "3,6",
        "3,5",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "2,4",
        "2,3",
        "3,3",
        "3,4",
        "4,4",
        "4,3",
        "4,2",
        "4,1",
        "3,1",
        "2,1",
        "1,1",
    ]
    assert simulation.effective_paths[0] == [
        "6,6",
        "6,5",
        "6,4",
        "6,3",
        "5,3",
        "5,4",
        "5,5",
        "5,6",
        "4,6",
        "3,6",
        "3,5",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "2,4",
        "2,3",
        "3,3",
        "3,4",
        "4,4",
        "4,3",
        "4,2",
        "4,1",
        "3,1",
        "2,1",
        "1,1",
    ]
    assert simulation.goals_found[0] == True
    assert simulation.visited_paths[0] == [
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (0, 2),
        (-1, -1),
        (-1, -1),
        (1, 2),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (0, 2),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
    ]

    # Path Test - Agent 2
    assert simulation.agent_searches[1] == [
        "6,6",
        "6,5",
        "6,4",
        "6,3",
        "5,3",
        "5,4",
        "5,5",
        "5,6",
        "4,6",
        "3,6",
        "3,5",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "2,4",
        "2,3",
        "3,3",
        "3,4",
        "4,4",
        "4,3",
        "4,2",
        "4,1",
        "3,1",
        "2,1",
        "1,1",
    ]
    assert simulation.effective_paths[1] == [
        "6,6",
        "6,5",
        "6,4",
        "6,3",
        "5,3",
        "5,4",
        "5,5",
        "5,6",
        "4,6",
        "3,6",
        "3,5",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "2,4",
        "2,3",
        "3,3",
        "3,4",
        "4,4",
        "4,3",
        "4,2",
        "4,1",
        "3,1",
        "2,1",
        "1,1",
    ]
    assert simulation.goals_found[1] == True
    assert simulation.visited_paths[1] == [
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (0, 2),
        (-1, -1),
        (-1, -1),
        (1, 2),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (0, 2),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
    ]

    # Path Test - Agent 3
    assert simulation.agent_searches[2] == [
        "6,6",
        "6,5",
        "6,4",
        "6,3",
        "6,2",
        "6,1",
        "5,1",
        "5,2",
        "5,1",
        "6,1",
        "6,2",
        "6,3",
        "6,4",
        "6,5",
        "6,6",
        "6,6",
    ]
    assert simulation.effective_paths[2] == []
    assert simulation.goals_found[2] == False
    assert simulation.visited_paths[2] == []