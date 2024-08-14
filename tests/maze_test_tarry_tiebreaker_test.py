from simulation.graph_utils import convert_maze
from simulation.simulation import Algorithm, Simulation


def test_simple_maze_tarry_tiebreaker_simulation():
    graph, rows, columns = convert_maze("test1.csv")

    simulation = Simulation(
        algorithm=Algorithm.TARRY_INTERVAL_TIE_BREAKER,
        n_agents=3,
        graph=graph,
        starting_node_id=f"{rows},{columns}",
    )

    simulation.simulate(shoud_print=False, should_print_trees=False)

    # Path Test - Agent 1
    # Starting Node
    assert simulation.agent_searches[0] == [
        "6,6",
        # TieBreaker Decision - Interval White
        "5,6",
        "4,6",
        # TieBreaker Decision - Interval White
        "3,6",
        "3,5",
        "3,4",
        # TieBreaker Decision - Interval White
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
    # Starting Node
    assert simulation.agent_searches[1] == [
        "6,6",
        # TieBreaker Decision - Interval White
        "6,5",
        # TieBreaker Decision - Interval White
        "5,5",
        "5,4",
        "4,4",
        "4,5",
        "4,6",
        # TieBreaker Decision - Interval Gray
        "3,6",
        "3,5",
        "3,4",
        # TieBreaker Decision - Interval Gray
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
    # Starting Node
    assert simulation.agent_searches[2] == [
        "6,6",
        # TieBreaker Decision - Interval Gray
        "6,5",
        # TieBreaker Decision - Interval White
        "6,4",
        # TieBreaker Decision - Interval White
        "6,3",
        # TieBreaker Decision - Interval White
        "5,3",
        # TieBreaker Decision - Interval White
        "4,3",
        # TieBreaker Decision - Interval White
        "3,3",
        # TieBreaker Decision - Interval Gray
        "3,4",
        # TieBreaker Decision - Interval Gray
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
