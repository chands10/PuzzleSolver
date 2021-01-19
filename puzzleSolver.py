from collections import Counter
import numpy as np
import time

class Solver(object):
    def __init__(self, board, constraints):
        self.board = board
        self.constraints = constraints
        self.given = set() # indices of given numbers
        self.quantities = Counter() # frequency of each number
        self.iterations = 0 # num iterations to solve board
        self.flipped = False # whether board is flipped or not
        self.numPos = 0 # number of positive numbers on board

    # i, j in bounds of board
    def validPoint(self, i, j):
        return 0 <= i < self.board.shape[0] and 0 <= j < self.board.shape[1]
    
    # f is ==, <, or <=
    # 1 1, 2 2s...7 7s by default, customizable in r
    def checkQuantity(self, f, r=range(1, 8)):
        for i in r:
            if not f(self.quantities[i], i):
                return False
        
        return True
            
    # check sum of row and number of positive numbers in row
    def checkRow(self, row, exact = False):
        l = len(row[row > 0])
        s = sum(row)
        
        if l > 4 or s > 20:
            return False
        elif l == 4 or exact:
            return s == 20 and l == 4
        elif l == 3: 
            # if sum less than 13 then would be impossible to sum to 20 with four numbers since 7 is the highest number
            # sum cannot be 20 with three numbers
            return 20 - 7 <= s < 20
        elif l == 2:
            return s >= 20 - 7 * 2
        
        return True
    
    #call check row on every row/col (used in isSolved)
    def checkLines(self):
        exact = True # sum of row must equal 20 with 4 numbers
        
        for row in self.board:
            if not self.checkRow(row, exact):
                return False
            
        transpose = self.board.T    
    
        for col in transpose:
            if not self.checkRow(col, exact):
                return False
            
        return True
    
    # check the whole board for 2x2s (used in isSolved)
    # return True if valid board
    def check2x2(self):
        for i in range(self.board.shape[0] - 1):
            for j in range(self.board.shape[1] - 1):
                if self.board[i][j] != 0 and self.board[i][j + 1] != 0 \
                   and self.board[i + 1][j] != 0 and self.board[i + 1][j + 1] != 0:
                    return False
                
        return True
    
    # check one square for 2x2s
    # return True if valid board
    def check2x2Square(self, i, j):    
        #left
        if self.posNum(i, j - 1):        
            # top left
            if self.posNum(i - 1, j) and self.posNum(i - 1, j - 1):
                return False
            
            #bottom left
            if self.posNum(i + 1, j) and self.posNum(i + 1, j - 1):
                return False
        
        # right
        if self.posNum(i, j + 1):
            # top right
            if self.posNum(i - 1, j) and self.posNum(i - 1, j + 1):
                return False
            
            # bottom right
            if self.posNum(i + 1, j) and self.posNum(i + 1, j + 1):
                return False
        
        return True
    
    # check if the current position contains a number > 0
    def posNum(self, i, j):
        if not self.validPoint(i, j):
            return False
        return self.board[i][j] > 0
    
    # check if the constraint at a certain row is met (helper function)
    def validConstraint(self, row, num, first):
        if first:
            val = 0
        else:
            val = -1
            
        return row[row > 0][val] == num
    
    # check constraints in dictionary r (defaults to all constraints)
    def checkConstraints(self, r={d:[i for i in range(7)] for d in ["top", "left", "bottom", "right"]}):
        transpose = self.board.T    
        
        # d = top, left, bottom, right
        for d in r:
            current = self.constraints[d]
            first = (d == "top" or d == "left")
            if d == "top" or d == "bottom":
                currentBoard = transpose
            else:
                currentBoard = self.board
                
            for i in r[d]:
                if current[i] != 0:
                    if not self.validConstraint(currentBoard[i], current[i], first):
                        return False
        
        return True
    
    # check that a certain position does not violate any constraints
    def checkConstraintSquare(self, i, j):
        r = {d: [j] for d in ["top", "left", "bottom", "right"]}
        r["left"] = [i]
        r["right"] = [i]
        
        # top and left work differently since we are iterating from top left to bottom right by row
        # check if this is the first number a constraint sees for top/left
        
        # top
        for k in range(i - 1, -1, -1):
            if self.board[k][j] != 0:
                del r["top"]
                break
        
        # left
        for k in range(j - 1, -1, -1):
            if self.board[i][k] != 0:
                del r["left"]
                break     
          
        # for bottom/right  
        # must wait until row/col is filled to check this constraint
        # since we are iterating from top left to bottom right row by row
        
        # bottom
        col = self.board.T[j]
        if len(col[col > 0]) != 4:
            del r["bottom"]
    
        # right
        row = self.board[i]
        if len(row[row > 0]) != 4:
            del r["right"]
                        
        return self.checkConstraints(r)    
    
    # used for connectedness property in isSolved
    # returns num positive squares visited and updates visited array
    def dfs(self, i, j, visited):
        if not self.validPoint(i, j):
            return 0
        
        if visited[i][j] == 1 or self.board[i][j] == 0:
            return 0
        
        visited[i][j] = 1
        
        return 1 + self.dfs(i + 1, j, visited) + \
        self.dfs(i - 1, j, visited) + \
        self.dfs(i, j + 1, visited) + \
        self.dfs(i, j - 1, visited)
    
    # check that an element can reach the last row fully traversed
    # using a modified dfs
    # called once for each positive element in a row with the same visited array
    # visited array may contain less rows than board,
    # the last row of the visited array represents the last row fully traversed
    def connected(self, i, j, visited, distinct):
        if not self.validPoint(i, j):
            return False
        
        # traversed this square before or this square is invalid
        if visited[i][j] == distinct or self.board[i][j] == 0:
            return False
        
        # reached a path from a previous element in the same original row that is connected
        if visited[i][j] > 0:
            return True
        
        if i == visited.shape[0] - 1: # last row fully traversed
            return True
        
        # mark visited with specific positive value for each element in row
        visited[i][j] = distinct
        
        return self.connected(i + 1, j, visited, distinct) or \
               self.connected(i - 1, j, visited, distinct) or \
               self.connected(i, j + 1, visited, distinct) or \
               self.connected(i, j - 1, visited, distinct)
    
    # check if the board is solved
    def isSolved(self):    
        f = lambda x, y: x == y
        
        if not self.checkQuantity(f):
            return False
        
        if not self.checkLines():
            return False
            
        # connected region
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] != 0:
                    root = (i, j)
                    break   
                
        visited = np.zeros_like(self.board)
        numVisited = self.dfs(root[0], root[1], visited)
    
        if not (numVisited == self.numPos == 28):
            return False
            
        if not self.check2x2():
            return False
                
        if not self.checkConstraints():
            return False
                
        return True
    
    
    # check if a position is valid
    def isValidSquare(self, i, j):
        f = lambda x, y: x <= y
        
        if not self.checkQuantity(f, [self.board[i][j]]):
            return False
        
        row = self.board[i]
        if not self.checkRow(row):
            return False
        
        col = self.board.T[j]
        if not self.checkRow(col):
            return False
        
        posRow = row[row > 0]
        posCol = col[col > 0]
        f = lambda x, y: x < y
        
        # if 3 numbers are filled in then we can find the final number in the line (20 - sum(line))
        # make sure there is enough quantity to fill in the final number
        if len(posRow) == 3 and not self.checkQuantity(f, [20 - sum(posRow)]):
            return False
        
        if len(posCol) == 3 and not self.checkQuantity(f, [20 - sum(posCol)]):
            return False
    
        if not self.check2x2Square(i, j):
            return False
        
        if not self.checkConstraintSquare(i, j):
            return False   
        
        return True 
    
    # check if board can ever be valid at this point going forward
    def canContinue(self, i, j):
        # get the line values up to i, j inclusive
        row = self.board[i][:j + 1]
        col = self.board.T[j][:i + 1]
                
        # must have filled in at least 4 - k numbers by this point of row/col
        posRowCount = len(row[row > 0])
        posColCount = len(col[col > 0])
        for k in range(4): 
            if j == 6 - k and posRowCount < 4 - k:
                return False
            
            if i == 6 - k and posColCount < 4 - k:
                return False    
                
        return True
    
    # driver function to solve board
    def solveBoard(self):
        # check if flipping vertically is faster
        if self.constraints["top"].count(0) > self.constraints["bottom"].count(0):
            self.flipped = True
            self.flipBoardVertically()
            print("Using flipped algorithm to go faster")    
            
        # fill in self.given and self.quantities
        self.given.clear()
        self.quantities.clear()
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] > 0:
                    self.given.add((i,j))
                    self.quantities[self.board[i][j]] += 1
        
        self.numPos = len(self.given)
                    
        t = time.time()
        solved = self.solveBoardHelper(0, 0)
        t = time.time() - t
        
        print("Iterations: {}".format(self.iterations))
        
        if self.flipped:
            self.flipBoardVertically() 
            
        print(self.board)
        if solved:
            print("Solved after {} seconds.".format(t))
        else:
            print("Found impossible to solve after {} seconds.".format(t))        
        return solved
    
    # recursive function to solve board
    def solveBoardHelper(self, rowIndex, colIndex):        
        #print(self.board)
        #input()
            
        self.iterations += 1
        
        if self.numPos == 28 and self.isSolved():
            return True                
        if self.numPos >= 28:
            return False
        
        if self.iterations % 1000 == 0:
            print(self.iterations)
            if 0:
                if self.flipped:
                    print(self.board[::-1])
                else:
                    print(self.board)
            
        for i in range(rowIndex, self.board.shape[0]):                        
            # check if this is the first time visiting a row for this
            # specific board by checking if we are at the first column
            # and we are at a square that has not been modified yet
            if i > 1 and colIndex == 0 and (self.board[i][0] == 0 or (i, 0) in self.given):
                # check connectedness property for row i - 2
                # by checking if each element in row i - 2 can reach an element
                # in row i - 1, since row i - 1 is the last completed row
                # (then eventually an element in row i - 1 can connect with an
                # element in row i)
                visited = np.zeros((i, self.board.shape[1])) # rows 0 to i - 1
                for j in range(self.board.shape[1]):
                    if self.board[i - 2][j] > 0 and not self.connected(i - 2, j, visited, j + 1):
                        return False
            
            for j in range(colIndex, self.board.shape[1]):
                og = self.board[i][j]
                
                # make sure constraints still hold at given number
                if (i, j) in self.given and not self.checkConstraintSquare(i, j):
                    return False
                    
                if self.board[i][j] < 7 and (i,j) not in self.given:
                    self.board[i][j] += 1
                    
                    # see if you can continue with a posNum
                    # (can update self.quantities and self.numPos after since
                    # self.canContinue does not rely on either)
                    if og == 0 and not self.canContinue(i, j):
                        self.board[i][j] = og
                        return False                   
                                            
                    if og == 0:
                        self.numPos += 1
                    self.quantities[og] -= 1
                    self.quantities[self.board[i][j]] += 1
                    while self.board[i][j] <= 7 and not self.isValidSquare(i, j):
                        self.quantities[self.board[i][j]] -= 1
                        self.board[i][j] += 1
                        self.quantities[self.board[i][j]] += 1
                        
                    if self.board[i][j] <= 7:
                        if self.solveBoardHelper(i, j):
                            return True
    
                    self.quantities[self.board[i][j]] -= 1                
                    self.board[i][j] = og
                    self.quantities[og] += 1
                    if og == 0:
                        self.numPos -= 1
                        
                    # see if you can continue with 0
                    if og == 0 and not self.canContinue(i, j):
                        return False
            
            colIndex = 0
                            
        return False
    
    # flip board and constraints
    def flipBoardVertically(self):
        self.constraints["bottom"], self.constraints["top"] = self.constraints["top"], self.constraints["bottom"]
        self.constraints["left"].reverse()
        self.constraints["right"].reverse()
        self.board = self.board[::-1]
    

if __name__ == "__main__":       
    # top left board
    constraints1 = {"top": [5,4,0,0,0,7,5], "left": [5,7,0,0,0,5,7], "bottom": [5,7,0,0,0,3,6], "right": [7,4,0,0,0,7,6]}
    
    board1 = np.zeros((7,7))
    board1[0][2] = 4
    board1[1][3] = 6
    board1[2][0] = 5
    board1[3][1] = 3
    board1[3][5] = 6
    board1[4][6] = 2
    board1[5][3] = 1
    board1[6][4] = 4
        
    # top right board
    constraints2 = {"top": [0,0,5,6,0,6,7], "left": [0,0,5,6,0,7,6], "bottom": [6,7,5,0,0,0,0], "right": [6,6,4,0,0,0,0]}
    
    board2 = np.zeros((7,7))
    board2[0][1] = 2
    board2[1][0] = 2
    board2[3][5] = 3
    board2[4][4] = 3
    board2[5][3] = 3
    board2[6][6] = 1
    
    # bottom left board
    constraints3 = {"top": [7,0,0,5,0,7,0], "left": [0,0,0,7,0,0,0], "bottom": [0,7,0,3,0,0,5], "right": [0,0,0,5,0,0,0]}
    
    board3 = np.zeros((7,7))
    board3[0][4] = 4
    board3[1][1] = 6
    board3[2][0] = 4
    board3[2][6] = 6
    board3[4][0] = 6
    board3[4][6] = 4
    board3[5][5] = 6
    board3[6][2] = 4
    
    #bottom right board
    constraints4 = {"top": [0] * 7, "left": [i for i in range(1, 8)], "bottom": [0,6,0,5,0,4,0], "right": [0,6,0,4,0,2,0]}
    
    board4 = np.zeros((7,7))
    board4[2][6] = 3
    board4[4][4] = 4
    board4[6][2] = 3   
    
    boards = [(board1, constraints1), (board2, constraints2), (board3, constraints3), (board4, constraints4)]
    
    while True:
        b = int(input("Pick a board from easy-hard (1,2,3,4): "))
        board, constraints = boards[b - 1]
        print("Board:")
        print(board)
        print("Constraints:")
        print(constraints)
        ans = input("Use this board? (y,n) ")
        if ans == "y":
            break
        
    solver = Solver(board, constraints)
    solved = solver.solveBoard()
