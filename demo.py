import argparse

from my import MyAlgorithm, TarryGeneralization
from pyamaze import COLOR, maze


def parse_arguments():
    parser = argparse.ArgumentParser(description="Maze exploration algorithm.")
    parser.add_argument(
        "--algorithm",
        type=str,
        default="self",
        help="Which algorithm should be used",
    )
    parser.add_argument(
        "--agents", type=int, default=3, help="Number of agents (default: 3)"
    )
    parser.add_argument(
        "--maze",
        type=str,
        default=None,
        help="File path to saved maze",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # Args
    args = parse_arguments()

    # Agent Colors
    colorList = [
        COLOR.red,
        COLOR.blue,
        COLOR.yellow,
        COLOR.orange,
        COLOR.pink,
        COLOR.cyan,
        COLOR.black,
    ]

    # Size of the maze
    numOfLines = 10
    numOfColumns = 10

    # Number of agents
    numOfAgents = args.agents

    # Create a instance of a maze
    m = maze(numOfLines, numOfColumns)
    
    if args.maze is not None:
        m.CreateMaze(loopPercent=0, theme="light", loadMaze=args.maze)
    else:
        m.CreateMaze(loopPercent=0, theme="light")

    # Algoritm Decision
    if args.algorithm == "self":
        # Implemented Algorithm
        myAlgorithm = MyAlgorithm(m, numOfAgents, colorList, start=None)
        steps, pionner_steps, fraction, fraction_pionner = myAlgorithm.run()
    elif args.algorithm == "tarry":
        # Tarry Generalization
        tarryGeneralization = TarryGeneralization(m, numOfAgents, colorList, start=None)
        steps, pionner_steps, fraction, last_steps = tarryGeneralization.run()
