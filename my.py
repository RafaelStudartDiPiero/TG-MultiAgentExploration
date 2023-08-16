from pyamaze import maze,agent,COLOR
import sys

# from collections import deque

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

class MyAlgorithm:
    def __init__(self, maze, start=None):
        self.maze = maze
        self.start = start
        self.compass = "NESW" # it establishes the children's storage order

    # Run the algorithm for all agents
    def run(self, numOfAgents):
        print("QUANTIDADE DE AGENTES: ", numOfAgents)
        print()

        division = 1.0 / numOfAgents
        paths = []
        for i in range(0, numOfAgents):
            start = i * division
            end = (i + 1) * division
            agentInterval = (start, end)
            agentColor = colorList[i % len(colorList)]
            mySearch, effective_path = self.run_single_agent(agentInterval)

            print("AGENTE ", i + 1)
            print("Cor: ", self.getColorString(agentColor))
            print("Intervalo: ", self.getIntervalString(agentInterval))
            print("Caminho eficaz pela árvore (representação mixed radix): ", self.getMixedRadixRepresentation(effective_path, self.maze))
            print()

            a = agent(self.maze,footprints=True,color=agentColor,shape='square',filled=True)

            paths.append({a:mySearch})


        # show only agent i
        # self.maze.tracePaths([paths[2]], kill=False, delay=100)

        #self.maze.tracePaths(paths, kill=False, delay=500)
        self.maze.tracePaths_by_key_press(paths, kill=False)

        self.maze.run()

    # Run the algorithm for a single agent
    def run_single_agent(self, agentInterval):
        if self.start is None:
            self.start = (self.maze.rows,self.maze.cols)

        explored = [self.start]
        mySearch = []

        parentList = []
        parentList.append((-1,-1))
        currCell = self.start
        agent_path = []
        effective_path = []

        count = 0

        while True:

            count += 1

            if currCell==self.maze._goal:
                mySearch.append(currCell)
                effective_path.append(currCell)
                break

            # If there are not visited children, go to parent
            nonVisitedChildren, allChildren = self.getChildrenPoints(currCell, self.maze.maze_map[currCell], parentList[-1], explored)
            count_nonVisitedChildren = len(nonVisitedChildren)
            if count_nonVisitedChildren == 0:
                explored.append(currCell)
                mySearch.append(currCell)
                currCell = parentList.pop()
                effective_path.pop()
                agent_path.pop()

                continue

            # Define the next step to the agent
            next = self.defineAgentNextStep(agentInterval, agent_path, allChildren, nonVisitedChildren)
            childCellPoint = allChildren[next]
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
    def getChildrenPoints(self, cellCoordinate, cellPoints, parent, explored):
        allChildren = []
        nonVisitedChildren = []
        for d in self.compass:
            if cellPoints[d] == True:
                if d=='N':
                    childCell = (cellCoordinate[0]-1,cellCoordinate[1])
                    if parent == childCell:
                        continue
                    if childCell in explored:
                        allChildren.append('N')
                        continue

                    allChildren.append('N')
                    nonVisitedChildren.append('N')
                elif d=='E':
                    childCell = (cellCoordinate[0],cellCoordinate[1]+1)
                    if parent == childCell:
                        continue
                    if childCell in explored:
                        allChildren.append('E')
                        continue

                    allChildren.append('E')
                    nonVisitedChildren.append('E')
                elif d=='S':
                    childCell = (cellCoordinate[0]+1,cellCoordinate[1])
                    if parent == childCell:
                        continue
                    if childCell in explored:
                        allChildren.append('S')
                        continue

                    allChildren.append('S')
                    nonVisitedChildren.append('S')
                elif d=='W':
                    childCell = (cellCoordinate[0],cellCoordinate[1]-1)
                    if parent == childCell:
                        continue
                    if childCell in explored:
                        allChildren.append('W')
                        continue

                    allChildren.append('W')
                    nonVisitedChildren.append('W')

        return nonVisitedChildren, allChildren

    def defineAgentNextStep(self, agentInterval, agent_path, allChildren, nonVisitedChildren):

        totalNumberOfChildren = len(allChildren)
        
        # If there is only 1 child just go on
        if totalNumberOfChildren == 1:
            agent_path.append((-1, -1))
            return 0
        
        # Get the weight interval of each node
        relative_node_weights = self.getRelativeNodeWeights(agent_path, totalNumberOfChildren)
        """ print("agentInterval: ", agentInterval)
        print("relative_node_weights: ", relative_node_weights)
        print("agent_path: ", agent_path)
        print("totalNumberOfChildren: ", totalNumberOfChildren) """

        # Return the first child that is able to obey the limits
        for i in range(0, totalNumberOfChildren):
            if (agentInterval[0] < relative_node_weights[i][1]) and (allChildren[i] in nonVisitedChildren):
                agent_path.append((i, totalNumberOfChildren))
                return i
            
        # Big weight agent in a light weight path
        # Go to any child that was not visited
        for i in range(0, totalNumberOfChildren):
            if allChildren[i] in nonVisitedChildren:
                agent_path.append((i, totalNumberOfChildren))
                return i

    def getRelativeNodeWeights(self, agent_path, count_children):

        # Calculating the previous node interval according the agent path
        path_size = len(agent_path)
        node_interval = (0, 1)
        if path_size > 0:
            if agent_path[0][0] != -1: # only if the first related node has more than one child
                chunk = 1 / agent_path[0][1]
                node_interval = (agent_path[0][0] * chunk,  agent_path[0][0] * chunk + chunk)

            for i in range(1, path_size):
                if agent_path[i][0] == -1:
                    continue

                node_interval_size = node_interval[1] - node_interval[0]
                chunk = node_interval_size / agent_path[i][1]
                node_interval = (node_interval[0] + agent_path[i][0] * chunk, node_interval[0] + agent_path[i][0] * chunk + chunk)

        # Calculating the weights of the next nodes
        weights = []
        node_interval_size = node_interval[1] - node_interval[0]
        chunk = node_interval_size / count_children
        start = 0
        end = 0
        for i in range(0, count_children):
            start = node_interval[0] + chunk * i
            end = start + chunk
            weight = (start, end)
            weights.append(weight)

        return weights

    # Auxiliary function to print agent color
    def getColorString(self, color):
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
        elif color == COLOR.pink:
            return "Rosa"
        elif color == COLOR.orange:
            return "Laranja"

    # Auxiliary function to print agent interval
    def getIntervalString(self, interval):
        if interval[1] > 0.9999:
            return "[" + str(interval[0]) + ", 1]"
        else:
            return "[" + str(interval[0]) + ", " + str(interval[1]) + "["
        
    # Auxiliary function to print the next direction
    def next_direction(self, current, next):
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
    def getMixedRadixRepresentation(self, effective_path, maze):
        mixedRadix = [(0, 0)]
        
        for i in range(0, len(effective_path) - 1):
            radix = 0
            next = self.next_direction(effective_path[i], effective_path[i + 1])

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

            """ print("directions: ", directions)
            print("atual: ", effective_path[i])
            print("próximo: ", effective_path[i+1])
            print("next: ", next) """
            digit = directions.index(next)
            #digit = 500

            if radix == 1:
                radix = "X"
                digit = "X"

            mixedRadix.append((digit, radix))

        return mixedRadix
    

class TarryGeneralization:
    def __init__(self):
        pass



colorList = [COLOR.red, COLOR.blue, COLOR.yellow, COLOR.orange, COLOR.pink, COLOR.cyan, COLOR.black]

numOfLines = 4
numOfColumns = 4

numOfAgents = 5
test = "testdummy.csv"

# Exemplo de execução com descrição passo a passo dos agentes
# python3 my.py 3 test1
if len(sys.argv) == 3:
    numOfAgents = int(sys.argv[1])
    test = sys.argv[2] + ".csv"


m=maze(numOfLines,numOfColumns)
m.CreateMaze(theme='light', loadMaze=test)
#m.CreateMaze(loopPercent=50,theme='light', saveMaze=True)
#m.CreateMaze(theme='light', saveMaze=True)

""" bSearch,bfsPath,fwdPath=BFS(m)
a=agent(m,footprints=True,color=COLOR.yellow,shape='square',filled=True)
bSearch2,bfsPath2,fwdPath2=BFS(m,(5,4))
a2=agent(m,footprints=True,color=COLOR.red,shape='square',filled=True)
m.tracePaths([{a:bSearch}, {a2:bSearch2}],delay=100) """



myAlgorithm = MyAlgorithm(m, start=None)
myAlgorithm.run(numOfAgents)
