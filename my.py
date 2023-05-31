from pyamaze import maze,agent,textLabel,COLOR
from collections import deque

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
#compass = "WSEN"

def my(m, agentWeight, start=None):
    if start is None:
        start=(m.rows,m.cols)

    explored = [start]
    mySearch=[]

    parentList = deque()
    parentList.append((-1,-1))
    currCell = start
    agent_path = []

    count = 0

    while True:

        count += 1

        if currCell==m._goal:
            mySearch.append(currCell)
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
            else:
                print(count)
                print(len(agent_path))
                print("verificar o que ocorre aqui")

            continue

        # Define the next step to the agent
        next = defineAgentNextStep(agentWeight, count_children, agent_path)
        childCellPoint = currentChildren[next]
        parentList.append(currCell)
        explored.append(currCell)
        mySearch.append(currCell)
        if childCellPoint=='N':
            currCell = (currCell[0]-1,currCell[1])
        elif childCellPoint=='E':
            currCell = (currCell[0],currCell[1]+1)
        elif childCellPoint=='S':
            currCell = (currCell[0]+1,currCell[1])     
        elif childCellPoint=='W':
            currCell = (currCell[0],currCell[1]-1)

    return mySearch

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

def defineAgentNextStep(agentWeight, count_children, agent_path):
      
    # If there is only 1 child just go on
    if count_children == 1:
        agent_path.append((-1, -1))
        return 0
    
    # Get the weight interval of each node
    relative_node_weights = getRelativeNodeWeights(agent_path, count_children)

    # Return the first child that is able to obey the limits
    for i in range(0, count_children):
        if agentWeight[0] < relative_node_weights[i][1]:
            agent_path.append((i, count_children))
            return i
        
    # Big weight agent in a light weight path
    print("big weight agent in a light weight path")
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




colorList = [COLOR.red, COLOR.green, COLOR.blue, COLOR.yellow, COLOR.cyan, COLOR.black]


if __name__=='__main__':

    numOfLines = 13
    numOfColumns = 13

    m=maze(numOfLines,numOfColumns)
    m.CreateMaze(loopPercent=10,theme='light', loadMaze='test2.csv')
    #m.CreateMaze(loopPercent=10,theme='light', saveMaze=True)

    """ bSearch,bfsPath,fwdPath=BFS(m)
    a=agent(m,footprints=True,color=COLOR.yellow,shape='square',filled=True)
    bSearch2,bfsPath2,fwdPath2=BFS(m,(5,4))
    a2=agent(m,footprints=True,color=COLOR.red,shape='square',filled=True)
    m.tracePaths([{a:bSearch}, {a2:bSearch2}],delay=100) """

    # posicional vs unário
    # seed -> gerar o mesmo valor aleatório

    numOfAgents = 50
    division = 1.0 / numOfAgents
    paths = []
    for i in range(0, numOfAgents):
        start = i * division
        end = (i + 1) * division
        agentWeight = (start, end)

        mySearch = my(m, agentWeight)
        agentColor = colorList[i % len(colorList)]
        a = agent(m,footprints=True,color=agentColor,shape='square',filled=True)

        """ # test 3
        mySearch = my(m, agentWeight, start=(7,7))
        agentColor = colorList[i % len(colorList)]
        a = agent(m,x=7,y=7,footprints=True,color=agentColor,shape='square',filled=True) """

        paths.append({a:mySearch})


    # only agent x
    #m.tracePaths([paths[2]], kill=False, delay=100)

    m.tracePaths(paths, kill=False, delay=300)

    m.run()


'''
Avisos para o professor:
- O algoritmo não grava todo o percurso do agente. Se, por exemplo, ele retorna para um nó pai, o filho é desconsiderado

'''