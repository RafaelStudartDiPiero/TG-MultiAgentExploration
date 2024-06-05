from simulation.graph_utils import convert_maze
from simulation.simulation import Algorithm, Simulation


def test_imperfect_maze_simulation():
    graph, rows, columns = convert_maze("testimperfect.csv")

    simulation = Simulation(
        algorithm=Algorithm.SELF,
        n_agents=3,
        graph=graph,
        starting_node_id=f"{rows},{columns}",
    )

    simulation.simulate(shoud_print=False, should_print_trees=False)

    # Metrics Test
    assert simulation.total_steps == 46
    assert simulation.pioneer_steps == 10
    assert simulation.fraction_explored - 1 < 0.0001
    assert simulation.fraction_pioneer - 0.80555 < 0.0001

    # Path Test - Agent 1
    assert simulation.agent_searches[0] == [
        "4,4",
        "3,4",
        "2,4",
        "1,4",
        "1,3",
        "2,3",
        "3,3",
        "3,2",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.effective_paths[0] == [
        "4,4",
        "3,4",
        "2,4",
        "1,4",
        "1,3",
        "2,3",
        "3,3",
        "3,2",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.goals_found[0] == True
    assert simulation.visited_paths[0] == [
        (0, 2),
        (0, 2),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (0, 2),
        (0, 2),
        (-1, -1),
    ]

    # Path Test - Agent 2
    assert simulation.agent_searches[1] == [
        "4,4",
        "3,4",
        "3,3",
        "2,3",
        "1,3",
        "1,4",
        "2,4",
        "1,4",
        "1,3",
        "2,3",
        "3,3",
        "3,2",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.effective_paths[1] == [
        "4,4",
        "3,4",
        "3,3",
        "3,2",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.goals_found[1] == True
    assert simulation.visited_paths[1] == [
        (0, 2),
        (1, 2),
        (1, 2),
        (0, 2),
        (0, 2),
        (-1, -1),
    ]

    # Path Test - Agent 3
    assert simulation.agent_searches[2] == [
        "4,4",
        "4,3",
        "4,2",
        "3,2",
        "3,3",
        "2,3",
        "1,3",
        "1,4",
        "2,4",
        "3,4",
        "2,4",
        "1,4",
        "1,3",
        "2,3",
        "3,3",
        "3,2",
        "4,2",
        "4,1",
        "3,1",
        "2,1",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.effective_paths[2] == [
        "4,4",
        "4,3",
        "4,2",
        "4,1",
        "3,1",
        "2,1",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.goals_found[2] == True
    assert simulation.visited_paths[2] == [
        (1, 2),
        (-1, -1),
        (1, 2),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
    ]
