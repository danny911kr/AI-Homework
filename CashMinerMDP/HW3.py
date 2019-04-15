import time
class MDP:
    def __init__(self):
        self.gridsize = 0
        self.wallpos = {}
        self.terminalpos = {}
        self.transitionProb = 0.0
        self.rewards = 0.0
        self.gamma = 0.0
        self.epsilon = 0.001
        self.actions = ('U', 'D', 'L', 'R', 'E', 'N')
        self.startTime = 0
        #U: up, D: down, L: left, R: right, E: exit, N: wall

        self.rewardsDict = {}
        self.transitionDict = {}

    def initialize(self, inputFile):
        inputData = open(inputFile, 'r')
        self.gridsize = int(inputData.readline().rstrip('\n'))
        wallsize = int(inputData.readline().rstrip('\n'))
        for i in range(wallsize):
            wall = inputData.readline().rstrip('\n').split(",")
            self.wallpos[(int(wall[0]), int(wall[1]))] = 'None'
        terminalsize = int(inputData.readline().rstrip('\n'))
        for i in range(terminalsize):
            terminal = inputData.readline().rstrip('\n').split(",")
            self.terminalpos[(int(terminal[0]), int(terminal[1]))] = int(terminal[2])
        self.transitionProb = float(inputData.readline().rstrip('\n'))
        self.rewards = float(inputData.readline().rstrip('\n'))
        self.gamma = float(inputData.readline().rstrip('\n'))

    def makeRewardsMatrix(self):
        for row in range(1, self.gridsize+1):
            for col in range(1, self.gridsize+1):
                if (row, col) in self.wallpos:
                    self.rewardsDict[(row, col)] = None
                elif (row, col) in self.terminalpos:
                    self.rewardsDict[(row, col)] = self.terminalpos[(row, col)]
                else:
                    self.rewardsDict[(row, col)] = self.rewards

    def isWall(self, row, col):
        if (row, col) not in self.rewardsDict: #it means that the current position is on edge.
            return True
        if self.rewardsDict[(row, col)] is None:
            return True
        return False

    def isExit(self, row, col):
        if (row,col) in self.terminalpos:
            return True
        return False

    def moveUp(self, row, col):
        upTranisition = []
        tempTransition = {}
        tempTransition[(row, col)] = 0
        tempTransition[(row-1, col-1)] = 0
        tempTransition[(row-1, col)] = 0
        tempTransition[(row-1, col+1)] = 0

        if self.isWall(row-1, col-1):
            tempTransition[(row, col)] += (1 - self.transitionProb) / 2
        else:
            tempTransition[(row-1, col-1)] += (1 - self.transitionProb) / 2

        if self.isWall(row-1, col):
            tempTransition[(row, col)] += self.transitionProb
        else:
            tempTransition[(row-1, col)] += self.transitionProb

        if self.isWall(row-1, col+1):
            tempTransition[(row, col)] += (1 - self.transitionProb) / 2
        else:
            tempTransition[(row-1, col+1)] += (1 - self.transitionProb) / 2

        for key, value in tempTransition.iteritems():
            if value != 0:
                upTranisition.append((value, key))
        return upTranisition

    def moveDown(self, row, col):
        downTransition = []
        tempTransition = {}
        tempTransition[(row, col)] = 0
        tempTransition[(row + 1, col - 1)] = 0
        tempTransition[(row + 1, col)] = 0
        tempTransition[(row + 1, col + 1)] = 0

        if self.isWall(row + 1, col - 1):
            tempTransition[(row, col)] += (1 - self.transitionProb) / 2
        else:
            tempTransition[(row + 1, col - 1)] += (1 - self.transitionProb) / 2

        if self.isWall(row + 1, col):
            tempTransition[(row, col)] += self.transitionProb
        else:
            tempTransition[(row + 1, col)] += self.transitionProb

        if self.isWall(row + 1, col + 1):
            tempTransition[(row, col)] += (1 - self.transitionProb) / 2
        else:
            tempTransition[(row + 1, col + 1)] += (1 - self.transitionProb) / 2

        for key, value in tempTransition.iteritems():
            if value != 0:
                downTransition.append((value, key))
        return downTransition

    def moveRight(self, row, col):
        rightTransition = []
        tempTransition = {}
        tempTransition[(row, col)] = 0
        tempTransition[(row - 1, col + 1)] = 0
        tempTransition[(row, col + 1)] = 0
        tempTransition[(row + 1, col + 1)] = 0

        if self.isWall(row - 1, col + 1):
            tempTransition[(row, col)] += (1 - self.transitionProb) / 2
        else:
            tempTransition[(row - 1, col + 1)] += (1 - self.transitionProb) / 2

        if self.isWall(row, col + 1):
            tempTransition[(row, col)] += self.transitionProb
        else:
            tempTransition[(row, col + 1)] += self.transitionProb

        if self.isWall(row + 1, col + 1):
            tempTransition[(row, col)] += (1 - self.transitionProb) / 2
        else:
            tempTransition[(row + 1, col + 1)] += (1 - self.transitionProb) / 2

        for key, value in tempTransition.iteritems():
            if value != 0:
                rightTransition.append((value, key))
        return rightTransition

    def moveLeft(self, row, col):
        leftTransition = []
        tempTransition = {}
        tempTransition[(row, col)] = 0
        tempTransition[(row - 1, col - 1)] = 0
        tempTransition[(row, col - 1)] = 0
        tempTransition[(row + 1, col - 1)] = 0

        if self.isWall(row - 1, col - 1):
            tempTransition[(row, col)] += (1 - self.transitionProb) / 2
        else:
            tempTransition[(row - 1, col - 1)] += (1 - self.transitionProb) / 2

        if self.isWall(row, col - 1):
            tempTransition[(row, col)] += self.transitionProb
        else:
            tempTransition[(row, col - 1)] += self.transitionProb

        if self.isWall(row + 1, col - 1):
            tempTransition[(row, col)] += (1 - self.transitionProb) / 2
        else:
            tempTransition[(row + 1, col - 1)] += (1 - self.transitionProb) / 2

        for key, value in tempTransition.iteritems():
            if value != 0:
                leftTransition.append((value, key))
        return leftTransition

    def makeTransitionMatrix(self):
        for row in range(1, self.gridsize+1):
            for col in range(1, self.gridsize+1):
                if self.isWall(row, col):
                    continue
                self.transitionDict[(row, col)] = {}
                if self.isExit(row, col):
                    self.transitionDict[(row, col)]['E'] = [(0.0, (row, col))]
                    continue
                self.transitionDict[(row, col)]['U'] = self.moveUp(row, col)
                self.transitionDict[(row, col)]['D'] = self.moveDown(row, col)
                self.transitionDict[(row, col)]['R'] = self.moveRight(row, col)
                self.transitionDict[(row, col)]['L'] = self.moveLeft(row, col)

    def getActionsPerState(self, state):
        return self.transitionDict[state].keys()

    def getTransitionPerAction(self, state, action):
        return self.transitionDict[state][action]

    def valueIteration(self):
        states = self.transitionDict.keys()
        utilityMatrix = {state: 0 for state in states}

        while True:
            beforeUtility = utilityMatrix.copy()
            maximumChange = 0

            for state in states:
                maximumValue =  max([sum([transition * utilityMatrix[movestate] for (transition, movestate) in
                                          self.getTransitionPerAction(state, action)]) for action in self.getActionsPerState(state)])
                utilityMatrix[state] = self.rewardsDict[state] + self.gamma * maximumValue
                maximumChange = max(maximumChange, abs(utilityMatrix[state]-beforeUtility[state]))

            if maximumChange < self.epsilon * (1-self.gamma) / self.gamma or time.time()-self.startTime >= 25:
                return beforeUtility

    def policyExtract(self, optimalUtility):
        states = self.transitionDict.keys()
        policy = {}
        for state in states:
            maxActionUtility = float('-inf')
            actionPolicy = None
            for action in self.getActionsPerState(state):
                sumValue = sum([transition * optimalUtility[movestate] for (transition, movestate) in self.getTransitionPerAction(state, action)])
                actionUtility = self.rewardsDict[state] + self.gamma * sumValue
                if actionUtility > maxActionUtility:
                    maxActionUtility = actionUtility
                    actionPolicy = action
            policy[state] = actionPolicy
        return policy

    def output(self, policy):
        result = [['N' for row in range(self.gridsize)] for col in range(self.gridsize)]
        for key, value in policy.iteritems():
            result[key[0]-1][key[1]-1]=value

        output_file = open("output.txt", "w")
        for row in range(self.gridsize):
            for col in range(self.gridsize):
                output_file.write(str(result[row][col]))
                if col != (self.gridsize-1):
                    output_file.write(",")
            output_file.write("\n")


    def executeMDP(self, filename):
        self.startTime = time.time()
        self.initialize(filename)
        self.makeRewardsMatrix()
        self.makeTransitionMatrix()
        optimalUtility = self.valueIteration()
        optimalPolicy = self.policyExtract(optimalUtility)
        self.output(optimalPolicy)

mdp = MDP()
mdp.executeMDP('input.txt')