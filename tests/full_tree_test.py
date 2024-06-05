from simulation.graph_utils import load_graph
from simulation.simulation import Algorithm, Simulation


def test_full_tree_simulation():
    graph = load_graph("full_tree_test.graphml")

    simulation = Simulation(
        algorithm=Algorithm.SELF,
        n_agents=3,
        graph=graph,
        starting_node_id="1",
        is_maze=False,
    )

    simulation.simulate(shoud_print=False, should_print_trees=False)

    # Metrics Test
    # assert simulation.total_steps == 43
    # assert simulation.pioneer_steps == 3
    # assert abs(simulation.fraction_explored - 0.78947) < 0.0001
    # assert abs(simulation.fraction_pioneer - 0.31578) < 0.0001

    # # Path Test - Agent 1
    # assert simulation.agent_searches[0] == [
    #     "1",
    #     "2",
    #     "4",
    #     "8",
    #     "16",
    #     "8",
    #     "17",
    #     "8",
    #     "4",
    #     "9",
    #     "18",
    #     "9",
    #     "19",
    #     "9",
    #     "4",
    #     "2",
    #     "5",
    #     "10",
    #     "5",
    #     "11",
    #     "5",
    #     "2",
    #     "1",
    #     "3",
    #     "6",
    #     "12",
    #     "6",
    #     "13",
    # ]
    # assert simulation.effective_paths[0] == ["1", "3", "6", "13"]
    # assert simulation.goals_found[0] == True
    # assert simulation.visited_paths[0] == [(1, 2), (0, 2), (1, 2)]

    # # Path Test - Agent 2
    # assert simulation.agent_searches[1] == [
    #     "1",
    #     "2",
    #     "5",
    #     "10",
    #     "5",
    #     "11",
    #     "5",
    #     "2",
    #     "1",
    #     "3",
    #     "6",
    #     "12",
    #     "6",
    #     "13",
    # # ]
    # assert simulation.effective_paths[1] == ["1", "3", "6", "13"]
    # assert simulation.goals_found[1] == True
    # assert simulation.visited_paths[1] == [(1, 2), (0, 2), (1, 2)]

    # Path Test - Agent 3
    assert simulation.agent_searches[2] == ["1", "3", "6", "13"]
    assert simulation.effective_paths[2] == ["1", "3", "6", "13"]
    assert simulation.goals_found[2] == True
    assert simulation.visited_paths[2] == [(1, 2), (0, 2), (1, 2)]
