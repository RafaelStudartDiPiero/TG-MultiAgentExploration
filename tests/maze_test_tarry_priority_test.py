from simulation.graph_utils import convert_maze
from simulation.simulation import Algorithm, Simulation


def test_simple_maze_tarry_priority_simulation():
    graph, rows, columns = convert_maze("test1.csv")

    simulation = Simulation(
        algorithm=Algorithm.TARRY_INTERVAL_PRIORITY,
        n_agents=3,
        graph=graph,
        starting_node_id=f"{rows},{columns}",
    )

    simulation.simulate(shoud_print=False, should_print_trees=False)

    # Path Test - Agent 1
    assert simulation.agent_searches[0] == [
        "6,6",
        # Priority - Interval Decision
        "5,6",
        "4,6",
        # Priority - Interval Decision
        "3,6",
        "3,5",
        "3,4",
        # Priority - Interval Decision
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

    # Path Test - Agent 2
    assert simulation.agent_searches[1] == [
        "6,6",
        # Priority - Interval Decision
        "5,6",
        "4,6",
        # Priority - Interval Decision
        "4,5",
        "4,4",
        "5,4",
        "5,5",
        "6,5",
        # Priority - Interval Decision
        "6,4",
        "6,3",
        "5,3",
        "5,2",
        "5,1",
        "4,1",
        "4,2",
        "4,3",
        # Tarry - Pioneer Arrived At Decision. Go Back to LCL
        "4,2",
        "4,1",
        "5,1",
        "5,2",
        "5,3",
        "6,3",
        "6,4",
        "6,5",
        "5,5",
        "5,4",
        "4,4",
        "4,5",
        # Tarry - LCL - Follow Path
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

    # Path Test - Agent 3
    assert simulation.agent_searches[2] == [
        "6,6",
        # Priority - Interval Decision
        "6,5",
        # Priority - Interval Decision
        "5,5",
        "5,4",
        "4,4",
        "4,5",
        "4,6",
        # Priority - Interval Decision
        "5,6",
        # Interval - Notice Loop - Start Going Back
        "4,6",
        "4,5",
        "4,4",
        "5,4",
        "5,5",
        "6,5",
        # Priority - Interval Decision Back on Track
        "6,4",
        "6,3",
        # Tarry - Pioneer Arrived At Decision. Go Back to LCL
        "6,4",
        "6,5",
        # Tarry - LCL - Follow Path
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
