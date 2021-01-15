import numpy as np
import time

# i, j in bounds of board
def validPoint(board, i, j):
    return 0 <= i < board.shape[0] and 0 <= j < board.shape[1]

# f is == or <=
# 1 1, 2 2s...7 7s by default, customizable in r
def checkQuantity(board, f, r=range(1, 8)):
    for i in r:
        if not f(len(board[board == i]), i):
            return False
    
    return True
        
# check sum of row and number of positive numbers in row
def checkRow(row, exact = False):
    l = len(row[row > 0])
    s = sum(row)
    
    if l > 4 or s > 20:
        return False
    elif l == 4 or exact:
        return s == 20 and l == 4
    elif l == 3: 
        # if sum less than 13 then would be impossible to sum to 20 with four numbers since 7 is the highest number
        return s >= 20 - 7 
    elif l == 2:
        return s >= 20 - 7 * 2
    
    return True

#call check row on every row/col (used in isSolved)
def checkLines(board):
    exact = True # sum of row must equal 20 with 4 numbers
    
    for row in board:
        if not checkRow(row, exact):
            return False
        
    transpose = board.T    

    for col in transpose:
        if not checkRow(col, exact):
            return False
        
    return True

# check the whole board for 2x2s (used in isSolved)
# return True if valid board
def check2x2(board):
    for i in range(board.shape[0] - 1):
        for j in range(board.shape[1] - 1):
            if board[i][j] != 0 and board[i][j + 1] != 0 \
               and board[i + 1][j] != 0 and board[i + 1][j + 1] != 0:
                return False
            
    return True

# check one square for 2x2s
# return True if valid board
def check2x2Square(board, i, j):    
    #left
    if posNum(board, i, j - 1):        
        # top left
        if posNum(board, i - 1, j) and posNum(board, i - 1, j - 1):
            return False
        
        #bottom left
        if posNum(board, i + 1, j) and posNum(board, i + 1, j - 1):
            return False
    
    # right
    if posNum(board, i, j + 1):
        # top right
        if posNum(board, i - 1, j) and posNum(board, i - 1, j + 1):
            return False
        
        # bottom right
        if posNum(board, i + 1, j) and posNum(board, i + 1, j + 1):
            return False
    
    return True

# check if the current position contains a number > 0
def posNum(board, i, j):
    if not validPoint(board, i, j):
        return False
    return board[i][j] > 0

# check if the constraint at a certain row is met (helper function)
def validConstraint(row, num, first):
    if first:
        val = 0
    else:
        val = -1
        
    return row[row > 0][val] == num

# check constraints in dictionary r (defaults to all constraints)
def checkConstraints(board, constraints, r={d:[i for i in range(7)] for d in ["top", "left", "bottom", "right"]}):
    transpose = board.T    
    
    # d = top, left, bottom, right
    for d in r:
        current = constraints[d]
        first = (d == "top" or d == "left")
        if d == "top" or d == "bottom":
            currentBoard = transpose
        else:
            currentBoard = board
            
        for i in r[d]:
            if current[i] != 0:
                if not validConstraint(currentBoard[i], current[i], first):
                    return False
    
    return True

# check that a certain position does not violate any constraints
def checkConstraintSquare(board, constraints, i, j):
    r = {d: [j] for d in ["top", "left", "bottom", "right"]}
    r["left"] = [i]
    r["right"] = [i]
    
    # top and left work differently since we are iterating from top left to bottom right by row
    # check if this is the first number a constraint sees for top/left
    
    # top
    for k in range(i - 1, -1, -1):
        if board[k][j] != 0:
            del r["top"]
            break
    
    # left
    for k in range(j - 1, -1, -1):
        if board[i][k] != 0:
            del r["left"]
            break     
      
    # for bottom/right  
    # must wait until row/col is filled to check this constraint
    # since we are iterating from top left to bottom right row by row
    
    # bottom
    col = board.T[j]
    if len(col[col > 0]) != 4:
        del r["bottom"]

    # right
    row = board[i]
    if len(row[row > 0]) != 4:
        del r["right"]
                    
    return checkConstraints(board, constraints, r)    

# used for connectedness property in isSolved
# updates visited array
def dfs(board, i, j, visited):
    if not validPoint(board, i, j):
        return
    
    if visited[i][j] == 1 or board[i][j] == 0:
        return
    
    visited[i][j] = 1
    
    dfs(board, i + 1, j, visited)
    dfs(board, i - 1, j, visited)
    dfs(board, i, j + 1, visited)
    dfs(board, i, j - 1, visited)

# check that an element can reach the last row fully traversed
# using a modified dfs
# called once for each positive element in a row with the same visited array
# visited array may contain less rows than board,
# the last row of the visited array represents the last row fully traversed
def connected(board, i, j, visited, distinct):
    if not validPoint(board, i, j):
        return False
    
    # traversed this square before or this square is invalid
    if visited[i][j] == distinct or board[i][j] == 0:
        return False
    
    # reached a path from a previous element in the same original row that is connected
    if visited[i][j] > 0:
        return True
    
    if i == visited.shape[0] - 1: # last row fully traversed
        return True
    
    # mark visited with specific positive value for each element in row
    visited[i][j] = distinct
    
    return connected(board, i + 1, j, visited, distinct) or \
           connected(board, i - 1, j, visited, distinct) or \
           connected(board, i, j + 1, visited, distinct) or \
           connected(board, i, j - 1, visited, distinct)

# check if the board is solved
def isSolved(board, constraints):    
    f = lambda x, y: x == y
    
    if not checkQuantity(board, f):
        return False
    
    if not checkLines(board):
        return False
        
    # connected region
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] != 0:
                root = (i, j)
                break   
            
    visited = np.zeros_like(board)
    dfs(board, root[0], root[1], visited)

    if not (len(visited[visited > 0]) == len(board[board > 0]) == 28):
        return False
        
    if not check2x2(board):
        return False
            
    if not checkConstraints(board, constraints):
        return False
            
    return True


# check if a position is valid
def isValidSquare(board, constraints, i, j):
    f = lambda x, y: x <= y
    
    if not checkQuantity(board, f, [board[i][j]]):
        return False
    
    row = board[i]
    if not checkRow(row):
        return False
    
    col = board.T[j]
    if not checkRow(col):
        return False    
                
    if not check2x2Square(board, i, j):
        return False
    
    if not checkConstraintSquare(board, constraints, i, j):
        return False   
    
    return True 

# check if board can ever be valid at this point going forward
def canContinue(board, i, j):
    row = board[i][:j + 1]
    col = board.T[j][:i + 1]
            
    # must have filled in at least 4 - k numbers by this point of row/col
    posRow = len(row[row > 0])
    posCol = len(col[col > 0])
    for k in range(4): 
        if j == 6 - k and posRow < 4 - k:
            return False
        
        if i == 6 - k and posCol < 4 - k:
            return False    
            
    return True

# recursive function to solve board
def solveBoard(board, constraints, given, iterations, flipped, rowIndex, colIndex):        
    #print(board)
    #input()
        
    # iterations acts as a pointer
    iterations[0] += 1
    
    l = len(board[board > 0])
    if l == 28 and isSolved(board, constraints):
        print("Iterations: {}".format(iterations[0]))
        return True                
    if l >= 28:
        return False
    
    if iterations[0] % 1000 == 0:
        print(iterations[0])
        if 0:
            if flipped:
                print(board[::-1])
            else:
                print(board)
        
    for i in range(rowIndex, board.shape[0]):                        
        # check connectedness property for row i - 2
        # by checking if each element in row i - 2 can reach an element
        # in row i - 1, since row i - 1 is the last completed row
        # (then eventually an element in row i - 1 can connect with an 
        # element in row i)
        if i > 1:
            visited = np.zeros((i, board.shape[1])) # rows 0 to i - 1
            for j in range(board.shape[1]):
                if board[i - 2][j] > 0 and not connected(board, i - 2, j, visited, j + 1):
                    return False
        
        for j in range(colIndex, board.shape[1]):
            og = board[i][j]
            
            # make sure constraints still hold at given number
            if (i, j) in given and not checkConstraintSquare(board, constraints, i, j):
                return False
                
            if board[i][j] < 7 and (i,j) not in given:
                board[i][j] += 1
                
                # see if you can continue with a posNum
                if og == 0 and not canContinue(board, i, j):
                    board[i][j] = og
                    return False   
                
                while board[i][j] <= 7 and not isValidSquare(board, constraints, i, j):
                    board[i][j] += 1
                    
                if board[i][j] <= 7:
                    if solveBoard(board, constraints, given, iterations, flipped, i, j):
                        return True
                
                board[i][j] = og
                # see if you can continue with 0
                if og == 0 and not canContinue(board, i, j):
                    return False
        
        colIndex = 0
                        
    return False

# flip board and constraints
# return new board
def flipBoardVertically(board, constraints):
    constraints["bottom"], constraints["top"] = constraints["top"], constraints["bottom"]
    constraints["left"].reverse()
    constraints["right"].reverse()
    board = board[::-1]
    return board
    

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
        
    # check if flipping vertically is faster
    flipped = False
    if constraints["top"].count(0) > constraints["bottom"].count(0):
        flipped = True
        board = flipBoardVertically(board, constraints)
        print("Using flipped algorithm to go faster")    
        
    given = set()
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] > 0:
                given.add((i,j))
                
    t = time.time()
    solved = solveBoard(board, constraints, given, [0], flipped, 0, 0)
    t = time.time() - t
    
    if flipped:
        board = flipBoardVertically(board, constraints)
        
    print(board)
    if solved:
        print("Solved after {} seconds.".format(t))
    else:
        print("Found impossible to solve after {} seconds.".format(t))
    