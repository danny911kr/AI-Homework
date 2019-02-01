#CSCI561 HW1 Lee Dong Ho
#Laser Checkmate game board ( Human vs AI )

import copy
class LaserCheckmateBoard:
    EMPTY = 0
    HUMAN = 1
    OPPONENT = 2
    BLOCK = 3
    HUMANLASER = 4
    OPPLASER = 5
    BOTHLASER = 6

    def __init__(self):
        self.size = 1
        self.board = []
        self.score = 0
        self.human = Player(self.HUMAN)
        self.opponent = Player(self.OPPONENT)

    # make a list of board from the input file
    def setBoard(self, inputFile):
        inputData = open(inputFile, 'r')
        # first row is size
        self.size = int(inputData.readline().rstrip('\n'))
        # parse the text file into the list
        for i in range(self.size):
            row = inputData.readline().rstrip('\n')
            rowInt = map(int, list(row))
            self.board.append(rowInt)
        # If there is a human or opponent in the file,
        # apply the move process to the board
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col]==self.human.num:
                    self.moveEffect(self.human,(row,col))
                if self.board[row][col]==self.opponent.num:
                    self.moveEffect(self.opponent,(row,col))

    # This printing function is for debugging
    def printBoard(self):
        for row in range(self.size):
            print ''
            for col in range(self.size):
                print self.board[row][col],

    # find the space that the player can go (value = 0)
    def validMoves(self):
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.EMPTY:
                    moves.append([row, col])
        return moves

    # Algorithm for applying laser effect
    def laserEffect(self, player, state):
        laser = 0
        if state == self.HUMANLASER and player.num == self.HUMAN:
            laser = self.HUMANLASER
        if state == self.OPPLASER and player.num == self.HUMAN:
            laser = self.BOTHLASER
        if state == self.HUMAN and player.num == self.HUMAN:
            laser = self.HUMANLASER
        if state == self.EMPTY and player.num == self.HUMAN:
            laser = self.HUMANLASER
        if state == self.OPPONENT and player.num == self.HUMAN:
            laser = self.OPPONENT
        if state == self.OPPLASER and player.num == self.OPPONENT:
            laser = self.OPPLASER
        if state == self.EMPTY and player.num == self.OPPONENT:
            laser = self.OPPLASER
        if state == self.HUMANLASER and player.num == self.OPPONENT:
            laser = self.BOTHLASER
        if state == self.OPPONENT and player.num == self.OPPONENT:
            laser = self.OPPLASER
        if state == self.HUMAN and player.num == self.OPPONENT:
            laser = self.HUMAN
        if state == self.BOTHLASER:
            laser = self.BOTHLASER
        return laser

    # Algorithm for applying move effect
    def moveEffect(self, player, move):

        #itself
        self.board[move[0]][move[1]] = self.laserEffect(player, self.board[move[0]][move[1]])

        #horizontal
        for i in range(1, 4):
            if move[1]+i >= self.size or self.board[move[0]][move[1]+i] == self.BLOCK:
                break
            self.board[move[0]][move[1]+i] = self.laserEffect(player, self.board[move[0]][move[1]+i])

        for i in range(1, 4):
            if move[1]-i < 0 or self.board[move[0]][move[1]-i] == self.BLOCK:
                break
            self.board[move[0]][move[1]-i] = self.laserEffect(player, self.board[move[0]][move[1]-i])

        #vertical
        for i in range(1, 4):
            if move[0] + i >= self.size or self.board[move[0] + i][move[1]] == self.BLOCK:
                break
            self.board[move[0] + i][move[1]] = self.laserEffect(player, self.board[move[0] + i][move[1]])

        for i in range(1, 4):
            if move[0] - i < 0 or self.board[move[0] - i][move[1]] == self.BLOCK:
                break
            self.board[move[0] - i][move[1]] = self.laserEffect(player, self.board[move[0] - i][move[1]])

        #diagonal
        for i in range(1, 4):
            if move[0]+i >= self.size or move[1]+i >= self.size or self.board[move[0]+i][move[1]+i] == self.BLOCK:
                break
            self.board[move[0]+i][move[1]+i] = self.laserEffect(player, self.board[move[0]+i][move[1]+i])

        for i in range(1, 4):
            if move[0]-i < 0 or move[1]-i < 0 or self.board[move[0]-i][move[1]-i] == self.BLOCK:
                break
            self.board[move[0]-i][move[1]-i] = self.laserEffect(player, self.board[move[0]-i][move[1]-i])

        for i in range(1, 4):
            if move[0]+i >= self.size or move[1]-i < 0 or self.board[move[0]+i][move[1]-i] == self.BLOCK:
                break
            self.board[move[0]+i][move[1]-i] = self.laserEffect(player, self.board[move[0]+i][move[1]-i])

        for i in range(1, 4):
            if move[0]-i < 0 or move[1]+i >= self.size or self.board[move[0]-i][move[1]+i] == self.BLOCK:
                break
            self.board[move[0]-i][move[1]+i] = self.laserEffect(player, self.board[move[0]-i][move[1]+i])

    # calculating score of player and opponent
    def boardScore(self):
        human = 0
        opponent = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.HUMAN:
                    human += 1
                if self.board[row][col] == self.OPPONENT:
                    opponent += 1
                if self.board[row][col] == self.HUMANLASER:
                    human += 1
                if self.board[row][col] == self.OPPLASER:
                    opponent += 1
                if self.board[row][col] == self.BOTHLASER:
                    human += 1
                    opponent += 1
        return human, opponent

    # execute move (move -> moveeffect -> lasereffect)
    def executeMove(self, player, validPosition):
        move = validPosition
        if player.num == self.HUMAN:
            self.board[move[0]][move[1]] = self.HUMAN  # Player's new position
        else:
            self.board[move[0]][move[1]] = self.OPPONENT  # Opponent's new position
        self.moveEffect(player, move)
        humanscore, opponentscore = self.boardScore()
        self.human.setScore(humanscore)
        self.opponent.setScore(opponentscore)

    # check whether the game is over
    def gameOver(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == int(self.EMPTY):
                    return False
        return True

# It can be both HUMAN and OPPONENT.
class Player:

    def __init__(self, playerNum):
        self.num = playerNum
        self.score = 0

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

# Game playing algorithm with alpha-beta pruning
class GamePlay:
    INFINITY = 1.0e400

    def __init__(self, board):
        self.board = board

    # score function of alpha-beta pruning
    def score(self, newboard):
        if newboard.human.getScore() > newboard.opponent.getScore():
            newboard.score = 1
        elif newboard.human.getScore() == newboard.opponent.getScore():
            newboard.score = 0
        if newboard.human.getScore() < newboard.opponent.getScore():
            newboard.score = -1
        return newboard.score

    # alpha-beta pruning algorithm
    def alphabetapruning(self, depth):
        move = []
        alpha = -self.INFINITY
        beta = self.INFINITY
        score = -self.INFINITY
        for m in board.validMoves():
            if depth == 0 or board.gameOver():
                self.score(board)
                return move
            newBoard = copy.deepcopy(board)
            newBoard.executeMove(newBoard.human, m)
            s = self.minAlphaBeta(newBoard, depth - 1, alpha, beta)
            if s == 1:
                move = m
                score = s
        return move, score

    def minAlphaBeta(self, board, depth, alpha, beta):
        if board.gameOver() or depth == 0:
            return self.score(board)
        score = self.INFINITY
        for m in board.validMoves():
            newBoard = copy.deepcopy(board)
            newBoard.executeMove(newBoard.opponent, m)
            s = self.maxAlphaBeta(newBoard, depth - 1, alpha, beta)
            score = min(score, s)
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score

    # higher bound
    def maxAlphaBeta(self, board, depth, alpha, beta):
        if board.gameOver() or depth == 0:
            return self.score(board)
        score = -self.INFINITY
        for m in board.validMoves():
            newBoard = copy.deepcopy(board)
            newBoard.executeMove(newBoard.human, m)
            s = self.minAlphaBeta(newBoard, depth - 1, alpha, beta)
            score = max(score, s)
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score

board = LaserCheckmateBoard()
board.setBoard('input.txt')
game = GamePlay(board)
move, score = game.alphabetapruning(5)
#print(move, score)

output_file = open("output.txt", "w")
#print move
output_file.write(str(move[0]) + " " + str(move[1]))
output_file.close()