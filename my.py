from pyamaze import maze,agent,COLOR
import sys
import random
import csv

class MyAlgorithm:
    def __init__(self, maze, numOfAgents, colorList, start=None):
        self.maze = maze
        self.numOfAgents = numOfAgents
        self.colorList = colorList
        self.start = start
        self.compass = "NESW" # it establishes the children's storage order

        if self.start is None:
            self.start = (self.maze.rows,self.maze.cols)

    # Run the algorithm
    def run(self):
        print("MY ALGORITHM - TRABALHO DE GRADUAÇÃO")
        print("QUANTIDADE DE AGENTES: ", self.numOfAgents)
        print()

        division = 1.0 / self.numOfAgents
        paths = []
        for i in range(0, self.numOfAgents):
            start = i * division
            end = (i + 1) * division
            agentInterval = (start, end)
            agentColor = self.colorList[i % len(self.colorList)]
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
        explored = [self.start]
        mySearch = []

        parentList = []
        parentList.append((-1,-1))
        currCell = self.start
        agent_path = []
        effective_path = []

        while True:

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

            digit = directions.index(next)

            if radix == 1:
                radix = "X"
                digit = "X"

            mixedRadix.append((digit, radix))

        return mixedRadix
    

class TarryGeneralization:
    def __init__(self, maze, numOfAgents, colorList, start=None):
        self.maze = maze
        self.numOfAgents = numOfAgents
        self.colorList = colorList
        self.start = start

        if self.start is None:
            self.start = (self.maze.rows,self.maze.cols)

    # Run the algorithm
    def run(self):
        """ print("GENERALIZATION OF TARRY'S ALGORITHM")
        print("QUANTIDADE DE AGENTES: ", self.numOfAgents)
        print() """

        paths = []
        agents_search, fraction = self.run_agents()
        pionner_steps = len(agents_search[0]) - 1 # Put the number of steps of the agent 1 and compare later
        totalSteps = 0

        for i in range(0, len(agents_search)):
            agentColor = self.colorList[i % len(self.colorList)]
            a = agent(self.maze,footprints=True,color=agentColor,shape='square',filled=True)
            paths.append({a:agents_search[i]})

            # Number of steps of the agent. Subtract 1 to consider that the first cell is not countable
            agent_steps = len(agents_search[i]) - 1

            # Count the total number of steps
            totalSteps += agent_steps

            # Get the number of the steps of the pionner
            pionner_steps = agent_steps if pionner_steps > agent_steps else pionner_steps


        # show only agent i
        # self.maze.tracePaths([paths[2]], kill=False, delay=100)

        """ self.maze.tracePaths(paths, kill=False, delay=50)
        #self.maze.tracePaths_by_key_press(paths, kill=False)

        self.maze.run() """

        #print("Total steps: ", totalSteps)

        return totalSteps, pionner_steps, fraction

    # Run the algorithm for all agents
    # The following steps come from the article "Multi-Agent Maze Exploration" - Kivelevitch and Cohen 2010
    def run_agents(self):

        # Matrix of the search of each agent
        agents_search = []

        # Matrix of the effective of each agent
        # It will be trully computed only in the PHASE 1 of the algorithm
        # In PHASE 2 it is useful only to know the effective path of the pionner agent
        effective_path = []

        # Matrix of the explored cells by each agent 
        agents_exploredCells = []

        # Array of the current cell of each agent
        agents_currentCell = []

        # Matrix of the parents list of each agent
        agents_parents = []

        # Array of the explored cells
        exploredCells = []
        exploredCells.append(self.start)

        # Array of dead-end cells
        deadEndCells = []

        # Array of booleans that indicates if an agent found the goal
        foundTheGoal = []

        # Matrix of the Last Common Location (LCL) of each agent related to the others
        lcl = []


        for i in range(0, self.numOfAgents):
            agents_search.append([self.start])
            effective_path.append([self.start])
            agents_exploredCells.append([self.start])
            agents_currentCell.append(self.start)
            agents_parents.append([(-1,-1)])
            foundTheGoal.append(False)
            lcl.append([])

            for j in range(0, self.numOfAgents):
                lcl[i].append(self.start)

        
        # Pay attention: this algorithm is divided in two phases. In the first phase, the agents
        # follow 6 steps until some agent finds the goal. If some agent finds the goal, the second
        # phase will start. In the second phase, the agents that doesn't find the goal, will go to
        # the Last Common Location (LCL) with the pionner agent, and then the agents will follow the
        # goal path

        # PHASE 1
        while True not in foundTheGoal:

            # During each loop all the agents follow the steps below
            # Step 1: The agent should move to cells that have not been traveled by any agent
            # Step 2: If there are several such cells, the agent should choose one arbitrarily
            # Step 3: If there is no cell that has not been traveled by an agent, the agent should prefer to move to a cell that has not been traveled by it
            # Step 4: If all the possible directions have already been traveled by the agent, or if the agent has reached a dead-end, the agent should retreat until a cell that meets one of the previous conditions
            # Step 5: All the steps should be logged by the agent in its history
            # Step 6: When retreating, mark the cells retreated from as “dead end”
            for i in range(0, self.numOfAgents):

                # If the agent found the goal, go to the next agent
                if foundTheGoal[i] == True:
                    continue

                # Get cell children
                currentCell = agents_currentCell[i]
                parent = agents_parents[i][-1]
                children = self.getChildren(currentCell, self.maze.maze_map[currentCell], parent)

                # Check cell children
                visited = []
                nonVisited = []
                for child in children:
                    if child not in deadEndCells:
                        if child in exploredCells:
                            visited.append(child)
                        else:
                            nonVisited.append(child)

                # If there is non visited cells, choose one arbitrarily
                if len(nonVisited) > 0:
                    # Update parents list
                    agents_parents[i].append(agents_currentCell[i])

                    # Go to child
                    agents_currentCell[i] = nonVisited[random.randint(0, len(nonVisited) - 1)]

                    # Update the general array of explored cells
                    if agents_currentCell[i] not in exploredCells:
                        exploredCells.append(agents_currentCell[i])

                    # Update the array of the explored cells by the agent
                    if agents_currentCell[i] not in agents_exploredCells[i]:
                        agents_exploredCells[i].append(agents_currentCell[i])

                    # Update agent's effective path
                    effective_path[i].append(agents_currentCell[i])

                # If there is no cell that has not been visted by an agent, the agent should prefer to move to a cell that has not been visted by it
                elif len(visited) > 0:
                    agent_nonVisited = []

                    for child in visited:
                        if child not in agents_exploredCells[i]:
                            agent_nonVisited.append(child)

                    # Update parents list
                    agents_parents[i].append(agents_currentCell[i])

                    # Go to child
                    agents_currentCell[i] = agent_nonVisited[random.randint(0, len(agent_nonVisited) - 1)]

                    # Update the array of the explored cells by the agent
                    agents_exploredCells[i].append(agents_currentCell[i])

                    # Update agent's effective path
                    effective_path[i].append(agents_currentCell[i])


                # No children - dead-end
                else:
                    deadEndCells.append(agents_currentCell[i])

                    # Go to parent
                    agents_currentCell[i] = agents_parents[i].pop()
                    effective_path[i].pop()

                # Update agent search path
                agents_search[i].append(agents_currentCell[i])

                # Update the Last Common Location (LCL) matrix if it is necessary
                for j in range(0, self.numOfAgents):
                    if i == j:
                        continue

                    if agents_currentCell[i] in effective_path[j]:
                        lcl[i][j] = agents_currentCell[i]
                        lcl[j][i] = agents_currentCell[i]

                # Check if the agent found the goal
                if agents_currentCell[i] == self.maze._goal:
                    foundTheGoal[i] = True
                    break

        # PHASE 2
        # Get the pionner index
        pionner = foundTheGoal.index(True)

        # From the article: "Given the path of the agent that was the 
        # first to find the exit, the pioneer, each agent has to find the last location
        # from its own-logged history that matches a location on the path
        # of the pioneer. This location is denoted Last Common Location (LCL)"
        for i in range(0, self.numOfAgents):
            if i == pionner:
                continue

            # Move agent until the last common location with the pionner agent
            comeback_index = -2
            while agents_search[i][-1] != lcl[pionner][i]:
                # Come back unitl the LCL
                agents_search[i].append(effective_path[i][comeback_index])
                comeback_index -= 1

            # Add the path from the last common location until the goal
            lcl_index = effective_path[pionner].index(lcl[pionner][i])
            split_index = lcl_index + 1
            agents_search[i] += effective_path[pionner][split_index:]

        # Get the explored fraction of the maze
        fraction = len(exploredCells) / (self.maze.rows * self.maze.cols)

        return agents_search, fraction
    
    # Return cell children 
    def getChildren(self, cellCoordinate, cellPoints, parent):
        children = []

        for d in "NESW":
            if cellPoints[d] == True:
                if d=='N':
                    childCell = (cellCoordinate[0]-1,cellCoordinate[1])
                    if parent == childCell:
                        continue

                    children.append(childCell)
                elif d=='E':
                    childCell = (cellCoordinate[0],cellCoordinate[1]+1)
                    if parent == childCell:
                        continue

                    children.append(childCell)
                elif d=='S':
                    childCell = (cellCoordinate[0]+1,cellCoordinate[1])
                    if parent == childCell:
                        continue

                    children.append(childCell)
                elif d=='W':
                    childCell = (cellCoordinate[0],cellCoordinate[1]-1)
                    if parent == childCell:
                        continue

                    children.append(childCell)

        return children


# List of colors of the agents
colorList = [COLOR.red, COLOR.blue, COLOR.yellow, COLOR.orange, COLOR.pink, COLOR.cyan, COLOR.black]

# Size of the maze
numOfLines = 10
numOfColumns = 10

# Number of agents
#numOfAgents = 8

# It will be used in the case of loading a specific maze
specificMaze = "somemaze.csv"

# In the case of loading a specific maze with pointed out number of agents. Example: python3 my.py 3 test1
if len(sys.argv) == 3:
    numOfAgents = int(sys.argv[1])
    specificMaze = sys.argv[2] + ".csv"

header = []
steps_row = []
pionner_steps_row = []

for i in range(1, 41):

    numOfAgents = i
    header.append(numOfAgents)

    pionner_stepsCount = 0
    stepsCount = 0
    fractionCount = 0
    iterations = 250

    for j in range(0, iterations):

        # Create a instance of a maze
        m=maze(numOfLines,numOfColumns)

        # Create a maze
        m.CreateMaze(loopPercent=0,theme='light')
        #m.CreateMaze(theme='light', loadMaze=specificMaze)
        #m.CreateMaze(loopPercent=0,theme='light', saveMaze=True)


        """ myAlgorithm = MyAlgorithm(m, numOfAgents, colorList, start=None)
        myAlgorithm.run() """

        tarryGeneralization = TarryGeneralization(m, numOfAgents, colorList, start=None)
        steps, pionner_steps, fraction = tarryGeneralization.run()

        stepsCount += steps
        pionner_stepsCount += pionner_steps
        fractionCount += fraction

    averageOfSteps = stepsCount / numOfAgents / iterations
    averageOfStepsOfThePionner = pionner_stepsCount / iterations
    averageOfFraction = fractionCount / iterations
    print(numOfAgents, " agents -> average number of steps: ", averageOfSteps)
    print(numOfAgents, " agents -> average number of pionner's steps: ", averageOfStepsOfThePionner)
    print(numOfAgents, " agents -> average number of explored fraction: ", averageOfFraction)

    steps_row.append(averageOfSteps)
    pionner_steps_row.append(averageOfStepsOfThePionner)

with  open("tarry_1to40agents_250iterations", "w") as f:
    writer = csv.writer(f)

    writer.writerow(header)
    writer.writerow(steps_row)
    writer.writerow(pionner_steps_row)

















""" bSearch,bfsPath,fwdPath=BFS(m)
a=agent(m,footprints=True,color=COLOR.yellow,shape='square',filled=True)
bSearch2,bfsPath2,fwdPath2=BFS(m,(5,4))
a2=agent(m,footprints=True,color=COLOR.red,shape='square',filled=True)
m.tracePaths([{a:bSearch}, {a2:bSearch2}],delay=100) """
