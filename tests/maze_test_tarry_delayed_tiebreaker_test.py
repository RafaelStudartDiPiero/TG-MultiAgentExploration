from simulation.graph_utils import convert_maze
from simulation.simulation import Algorithm, Simulation


def test_simple_maze_delayed_tiebreaker_simulation():
    graph, rows, columns = convert_maze("test1.csv")

    simulation = Simulation(
        algorithm=Algorithm.TARRY_DELAYED_INTERVAL_TIE_BREAKER,
        n_agents=3,
        graph=graph,
        starting_node_id=f"{rows},{columns}",
    )

    simulation.simulate(shoud_print=False, should_print_trees=False)

    # Path Test - Agent 1
    assert simulation.agent_searches[0] == [
        # Start
        "6,6",
        # Interval First Step
        "5,6",
        # Interval Second Step
        "4,6",
        # Tarry Decision - Interval White
        "3,6",
        "3,5",
        "3,4",
        # Tarry Decision - Interval White
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
    assert simulation.agent_searches[1][0:16] == [
        # Start
        "6,6",
        # Interval First Step
        "5,6",
        # Interval Second Step
        "4,6",
        # Tarry Decision - Interval White
        "4,5",
        "4,4",
        "5,4",
        "5,5",
        "6,5",
        # Tarry Decision - Interval White
        "6,4",
        "6,3",
        # Tarry Decision - Interval White
        "5,3",
        # Tarry Decision - Interval White
        "5,2",
        "5,1",
        # Tarry Decision - Interval White
        "4,1",
        "4,2",
        # Tarry Decision - Not Interval White
        "3,2",
        # Tarry - Pioneer Arrived At Decision. Go Back to LCL
        # Omitted
        # Tarry - LCL - Follow Path
        # Omitted
    ]

    # Path Test - Agent 3
    assert simulation.agent_searches[2][0:14] == [
        # Start
        "6,6",
        # Interval First Step
        "6,5",
        # Interval Second Step
        "5,5",
        # Start Tarry with Tiebreaker
        "5,4",
        "4,4",
        "4,5",
        "4,6",
        # Tarry Decision - Interval Gray
        "5,6",
        # Notice Loop - Step Back
        "4,6",
        # Tarry Decision - Not Interval Gray
        "3,6",
        "3,5",
        "3,4",
        # Tarry Decision - Not Interval White
        "3,3",
        "4,3",
        # Tarry Decision - Not Interval Gray - Random - Test Both
        # Tarry - Pioneer Arrived At Decision. Go Back to LCL
        # Omitted
        # Tarry - LCL - Follow Path
        # Omitted
    ]

    assert (
        simulation.agent_searches[2][14:16]
        == [
            # Tarry Decision - Not Interval Gray - Random - Test Both
            "5,3",
            # Tarry Decision - Not Interval Gray - Random - Test Both
            "5,2",
        ]
        or simulation.agent_searches[2][14:16]
        == [
            # Tarry Decision - Not Interval Gray - Random - Test Both
            "5,3",
            # Tarry Decision - Not Interval Gray - Random - Test Both
            "6,3",
        ]
    ) or (
        simulation.agent_searches[2][14:16]
        == [
            # Tarry Decision - Not Interval Gray - Random - Test Both
            "4,2",
            # Tarry Decision - Not Interval Gray - Random - Test Both
            "3,2",
        ]
        or simulation.agent_searches[2][14:16]
        == [
            # Tarry Decision - Not Interval Gray - Random - Test Both
            "4,2",
            # Tarry Decision - Not Interval Gray - Random - Test Both
            "4,1",
        ]
    )
