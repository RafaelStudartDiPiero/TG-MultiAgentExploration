from simulation.graph_utils import convert_maze
from simulation.simulation import Algorithm, Simulation


def test_simple_maze_simulation():
    graph, rows, columns = convert_maze("test1.csv")

    simulation = Simulation(
        algorithm=Algorithm.SELF,
        n_agents=3,
        graph=graph,
        starting_node_id=f"{rows},{columns}",
    )

    simulation.simulate(shoud_print=False, should_print_trees=False)

    # Metrics Test
    assert simulation.total_steps == 74
    assert simulation.pioneer_steps == 16
    assert simulation.fraction_explored - 0.8611111 < 0.0001
    assert simulation.fraction_pioneer - 0.80555 < 0.0001

    # Path Test - Agent 1
    assert simulation.agent_searches[0] == [
        "6,6",
        "5,6",
        "4,6",
        "3,6",
        "3,5",
        "3,4",
        "2,4",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "1,3",
        "2,3",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.effective_paths[0] == [
        "6,6",
        "5,6",
        "4,6",
        "3,6",
        "3,5",
        "3,4",
        "2,4",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "1,3",
        "2,3",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.goals_found[0] == True
    assert simulation.visited_paths[0] == [
        (0, 2),
        (-1, -1),
        (0, 2),
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
        "5,6",
        "4,6",
        "4,5",
        "4,4",
        "5,4",
        "5,5",
        "6,5",
        "6,4",
        "6,3",
        "5,3",
        "5,2",
        "5,1",
        "4,1",
        "4,2",
        "4,3",
        "3,3",
        "3,4",
        "2,4",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "1,3",
        "2,3",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.effective_paths[1] == [
        "6,6",
        "5,6",
        "4,6",
        "4,5",
        "4,4",
        "5,4",
        "5,5",
        "6,5",
        "6,4",
        "6,3",
        "5,3",
        "5,2",
        "5,1",
        "4,1",
        "4,2",
        "4,3",
        "3,3",
        "3,4",
        "2,4",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "1,3",
        "2,3",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.goals_found[1] == True
    assert simulation.visited_paths[1] == [
        (0, 2),
        (-1, -1),
        (1, 2),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (-1, -1),
        (0, 2),
        (1, 2),
        (-1, -1),
        (0, 2),
        (-1, -1),
        (1, 2),
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
        "5,5",
        "5,4",
        "4,4",
        "4,5",
        "4,6",
        "5,6",
        "4,6",
        "4,5",
        "4,4",
        "5,4",
        "5,5",
        "6,5",
        "6,4",
        "6,3",
        "5,3",
        "4,3",
        "3,3",
        "3,4",
        "2,4",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "1,3",
        "2,3",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.effective_paths[2] == [
        "6,6",
        "6,5",
        "6,4",
        "6,3",
        "5,3",
        "4,3",
        "3,3",
        "3,4",
        "2,4",
        "2,5",
        "2,6",
        "1,6",
        "1,5",
        "1,4",
        "1,3",
        "2,3",
        "2,2",
        "1,2",
        "1,1",
    ]
    assert simulation.goals_found[2] == True
    assert simulation.visited_paths[2] == [
        (1, 2),
        (1, 2),
        (-1, -1),
        (0, 2),
        (0, 2),
        (0, 2),
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
