from pyamaze import maze,agent,textLabel,COLOR
from collections import deque

def BFS(m,start=None):
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
    return bSearch,bfsPath,fwdPath


compass = "NESW"

def my(m, agentWeight, start=None):
    if start is None:
        start=(m.rows,m.cols)

    explored = [start]
    mySearch=[]

    parentList = deque()
    parentList.append((-1,-1))
    currCell = start
    root_count = 0
    tree_level = 1
    agent_path = []

    while root_count < 2:

        if currCell==m._goal:
            break

        # Checking if agent came back to root
        if currCell==start:
            root_count += 1
            if root_count > 10:
                print("voltei para a raiz. não sei o que fazer")
                break

        # If there are not children, go to parent
        currentChildren = getChildrenPoints(currCell, m.maze_map[currCell], parentList[0], explored)
        count_children = len(currentChildren)
        if count_children == 0:
            explored.append(currCell)
            mySearch.append(currCell)
            currCell = parentList.pop()
            tree_level -= 1
            agent_path.pop()
            continue

        # Define the next step to the agent
        next = defineAgentNextStep(agentWeight, count_children, tree_level, agent_path)
        childCellPoint = currentChildren[next]
        tree_level += 1
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

def defineAgentNextStep(agentWeight, count_children, tree_level, agent_path):
      
    if count_children == 1:
        agent_path.append(0.0)
        return 0
    
    division = (1.0 / count_children) * (10 ** (-(tree_level - 1)))

    # Return the first child that is able to obey the limits
    for i in range(0, count_children):
        threshold = division * (i + 1) + sum(agent_path)
        print("sum(agent_path): ", sum(agent_path))
        print("threshold: ", threshold)
        print("agentWeight[0]: ", agentWeight[0])
        print("tree_level: ", tree_level)
        if agentWeight[0] <= threshold:
            print("division * (i): ", division * (i))
            agent_path.append(division * (i))
            return i
        
    #return count_children - 1
    
    #ERROR
    print("ERROR - defineAgentNextStep")
    return None


colorList = [COLOR.red, COLOR.cyan, COLOR.green, COLOR.blue, COLOR.yellow, COLOR.black]


if __name__=='__main__':

    numOfLines = 20
    numOfColumns = 20

    m=maze(numOfLines,numOfColumns)
    m.CreateMaze(loopPercent=10,theme='light')

    """ bSearch,bfsPath,fwdPath=BFS(m)
    a=agent(m,footprints=True,color=COLOR.yellow,shape='square',filled=True)
    bSearch2,bfsPath2,fwdPath2=BFS(m,(5,4))
    a2=agent(m,footprints=True,color=COLOR.red,shape='square',filled=True)
    m.tracePaths([{a:bSearch}, {a2:bSearch2}],delay=100) """

    numOfAgents = 3
    division = 1.0 / numOfAgents
    paths = []
    for i in range(0, numOfAgents):
        start = i * division
        end = (i + 1) * division
        agentWeight = (start, end)
        mySearch = my(m, agentWeight)

        agentColor = colorList[i % len(colorList)]
        a = agent(m,footprints=True,color=agentColor,shape='square',filled=True)

        paths.append({a:mySearch})


    m.tracePaths(paths, delay=100)

    m.run()