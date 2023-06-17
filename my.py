from pyamaze import maze,agent,textLabel,COLOR
from collections import deque
import sys

""" def BFS(m,start=None):
    if start is None:
        start=(m.rows,m.cols)
    frontier = deque()
    frontier.append(start)
    bfsPath = {}
    explored = [start]
    bSearch=[]

    while len(frontier)>0:
        currCell=frontier.popleft()
        if currCell==m._goal:
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in explored:
                    continue
                frontier.append(childCell)
                explored.append(childCell)
                bfsPath[childCell] = currCell
                bSearch.append(childCell)
    # print(f'{bfsPath}')
    fwdPath={}
    cell=m._goal
    while cell!=start:
        fwdPath[bfsPath[cell]]=cell
        cell=bfsPath[cell]
    return bSearch,bfsPath,fwdPath """


compass = "NESW" # priority

def my(m, agentInterval, start=None):
    if start is None:
        start=(m.rows,m.cols)

    explored = [start]
    mySearch=[]

    parentList = deque()
    parentList.append((-1,-1))
    currCell = start
    agent_path = []
    effective_path = []

    count = 0

    while True:

        count += 1

        if currCell==m._goal:
            mySearch.append(currCell)
            effective_path.append(currCell)
            break

        # If there are not children, go to parent
        currentChildren = getChildrenPoints(currCell, m.maze_map[currCell], parentList[0], explored)
        count_children = len(currentChildren)
        if count_children == 0:
            explored.append(currCell)
            mySearch.append(currCell)
            currCell = parentList.pop()

            if len(agent_path) != 0:
                agent_path.pop()
                effective_path.pop()
            """ else:
                print(count)
                print(len(agent_path))
                print("verificar o que ocorre aqui") """

            continue

        # Define the next step to the agent
        next = defineAgentNextStep(agentInterval, count_children, agent_path)
        childCellPoint = currentChildren[next]
        parentList.append(currCell)
        explored.append(currCell)
        mySearch.append(currCell)
        effective_path.append(currCell)
        if childCellPoint=='N':
            currCell = (currCell[0]-1,currCell[1])
        elif childCellPoint=='E':
            currCell = (currCell[0],currCell[1]+1)
        elif childCellPoint=='S':
            currCell = (currCell[0]+1,currCell[1])     
        elif childCellPoint=='W':
            currCell = (currCell[0],currCell[1]-1)

    return mySearch, effective_path

# Return children's cardinal points in preferential order 
def getChildrenPoints(cellCoordinate, cellPoints, parent, explored):
    children = []
    for d in compass:
        if cellPoints[d] == True:
            if d=='N':
                childCell = (cellCoordinate[0]-1,cellCoordinate[1])
                if parent == childCell or childCell in explored:
                    continue
                else:
                    children.append('N')
            elif d=='E':
                childCell = (cellCoordinate[0],cellCoordinate[1]+1)
                if parent == childCell or childCell in explored:
                    continue
                else:
                    children.append('E')
            elif d=='S':
                childCell = (cellCoordinate[0]+1,cellCoordinate[1])
                if parent == childCell or childCell in explored:
                    continue
                else:
                    children.append('S')
            elif d=='W':
                childCell = (cellCoordinate[0],cellCoordinate[1]-1)
                if parent == childCell or childCell in explored:
                    continue
                else:
                    children.append('W')

    return children

def defineAgentNextStep(agentInterval, count_children, agent_path):
      
    # If there is only 1 child just go on
    if count_children == 1:
        agent_path.append((-1, -1))
        return 0
    
    # Get the weight interval of each node
    relative_node_weights = getRelativeNodeWeights(agent_path, count_children)

    # Return the first child that is able to obey the limits
    for i in range(0, count_children):
        if agentInterval[0] < relative_node_weights[i][1]:
            agent_path.append((i, count_children))
            return i
        
    # Big weight agent in a light weight path
    #print("big weight agent in a light weight path")
    return count_children - 1
    
    #ERROR
    #print("ERROR - defineAgentNextStep")
    #return None

def getRelativeNodeWeights(agent_path, count_children):

    # Calculating the previous interval according the agent path
    path_size = len(agent_path)
    interval = (0, 1)
    if path_size > 0:
        chunk = 1 / agent_path[0][1]
        interval = (agent_path[0][0] * chunk,  agent_path[0][0] * chunk + chunk)

        for i in range(1, path_size):
            if agent_path[i][0] == -1:
                continue

            interval_size = interval[1] - interval[0]
            chunk = interval_size / agent_path[i][1]
            interval = (interval[0], interval[0] + chunk)

    # Calculating the weights of the next nodes
    weights = []
    interval_size = interval[1] - interval[0]
    chunk = interval_size / count_children
    start = 0
    end = 0
    for i in range(0, count_children):
        start = interval[0] + chunk * i
        end = start + chunk
        weight = (start, end)
        weights.append(weight)

    return weights




colorList = [COLOR.red, COLOR.blue, COLOR.yellow, COLOR.cyan, COLOR.black]

# Auxiliary function to print agent color
def getColorString(color):
    if color == COLOR.red:
        return "Vermelho"
    elif color == COLOR.blue:
        return "Azul"
    elif color == COLOR.yellow:
        return "Amarelo"
    elif color == COLOR.cyan:
        return "Ciano"
    elif color == COLOR.black:
        return "Preto"

# Auxiliary function to print agent interval
def getIntervalString(interval):
    if interval[1] > 0.9999:
        return "[" + str(interval[0]) + ", 1]"
    else:
        return "[" + str(interval[0]) + ", " + str(interval[1]) + "["
    
# Auxiliary function to print the next direction
def next_direction(current, next):
    if current[0] != next[0]:
        if current[0] < next[0]:
            return "S"
        else:
            return "N"
    else:
        if current[1] < next[1]:
            return "E"
        else:
            return "W"

# Auxiliary function to get the mixed radix representation of the agent effective_path
def getMixedRadixRepresentation(effective_path, maze):
    mixedRadix = [(0, 0)]
    
    for i in range(0, len(effective_path) - 1):
        radix = 0
        next = next_direction(effective_path[i], effective_path[i + 1])

        directions = []
        if maze.maze_map[effective_path[i]]['N'] == 1 and (effective_path[i][0] - 1, effective_path[i][1]) != effective_path[i - 1]:
            radix += 1
            directions.append('N')
        if maze.maze_map[effective_path[i]]['E'] == 1 and (effective_path[i][0], effective_path[i][1] + 1) != effective_path[i - 1]:
            radix += 1
            directions.append('E')
        if maze.maze_map[effective_path[i]]['S'] == 1 and (effective_path[i][0] + 1, effective_path[i][1]) != effective_path[i - 1]:
            radix += 1
            directions.append('S')
        if maze.maze_map[effective_path[i]]['W'] == 1 and (effective_path[i][0], effective_path[i][1] - 1) != effective_path[i - 1]:
            radix += 1
            directions.append('W')

        digit = directions.index(next)

        if radix == 1:
            radix = "X"
            digit = "X"

        mixedRadix.append((digit, radix))

    return mixedRadix


if __name__=='__main__':

    numOfLines = 3
    numOfColumns = 3

    numOfAgents = 1
    test = "testdummy.csv"

    # Professor
    # python3 my.py 3 test1
    if len(sys.argv) == 3:
        numOfAgents = int(sys.argv[1])
        test = sys.argv[2] + ".csv"


    m=maze(numOfLines,numOfColumns)
    m.CreateMaze(loopPercent=10,theme='light', loadMaze=test)
    #m.CreateMaze(loopPercent=10,theme='light', saveMaze=True)
    #m.CreateMaze(theme='light', saveMaze=True)

    """ bSearch,bfsPath,fwdPath=BFS(m)
    a=agent(m,footprints=True,color=COLOR.yellow,shape='square',filled=True)
    bSearch2,bfsPath2,fwdPath2=BFS(m,(5,4))
    a2=agent(m,footprints=True,color=COLOR.red,shape='square',filled=True)
    m.tracePaths([{a:bSearch}, {a2:bSearch2}],delay=100) """

    # posicional vs unário
    # seed -> gerar o mesmo valor aleatório

    print("QUANTIDADE DE AGENTES: ", numOfAgents)
    print()

    division = 1.0 / numOfAgents
    paths = []
    for i in range(0, numOfAgents):
        start = i * division
        end = (i + 1) * division
        agentInterval = (start, end)
        agentColor = colorList[i % len(colorList)]
        mySearch, effective_path = my(m, agentInterval)

        if test == "test3.csv":
            mySearch, effective_path = my(m, agentInterval, start=(7,7))

        print("AGENTE ", i + 1)
        print("Cor: ", getColorString(agentColor))
        print("Intervalo: ", getIntervalString(agentInterval))
        print("Caminho eficaz pela árvore (representação mixed radix): ", getMixedRadixRepresentation(effective_path, m))
        print()

        a = agent(m,footprints=True,color=agentColor,shape='square',filled=True)

        if test == "test3.csv":
            a = agent(m,x=7,y=7,footprints=True,color=agentColor,shape='square',filled=True)

        paths.append({a:mySearch})


    # only agent x
    # m.tracePaths([paths[2]], kill=False, delay=100)

    #m.tracePaths(paths, kill=False, delay=500)
    m.tracePaths_by_key_press(paths, kill=False, delay=500)

    m.run()
