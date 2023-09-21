from pyamaze import maze

for i in range(0, 250):
    m=maze(20,20)
    filename = 'mazes/twenty_by_twenty/maze_20x20__' + str(i + 1)
    m.CreateMaze(loopPercent=0,theme='light', saveMaze=filename)