from pyamaze import maze

for i in range(0, 250):
    m=maze(100,100)
    filename = 'mazes/100_by_100/maze_100x100__' + str(i + 1)
    m.CreateMaze(loopPercent=0,theme='light', saveMaze=filename)

    # Free up memory
    m._win.destroy()