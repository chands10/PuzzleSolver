import numpy as np
from enum import Enum
import time
from math import comb
from functools import lru_cache

class Shape(Enum):
    leftFrown = '🕝'
    rightFrown = '🕤'
    
    # cups are unused in final solution
    # originally the program would determine if a square was a quart vs sliver before area was calculated, and we would go through all these combinations
    # but 90 million combinations are too many to brute force
    leftCup = '🕒'
    rightCup = '🕘'

EMPTY = '⚪'
FORCED_EMPTY = '⚫' # do not consider this square non-empty
diagonals = {'/': (Shape.leftFrown, Shape.rightCup),
             '\\': (Shape.rightFrown, Shape.leftCup)}
DEBUG = 0
class Direction(Enum):
    up = 1
    upright = 2
    right = 3
    downright = 4
    down = 5
    downleft = 6
    left = 7
    upleft = 8
    
def eqGrid(g1, g2):
    c1 = g1.copy()
    c2 = g2.copy()
    
    # set FORCED_EMPTY == EMPTY
    c1[c1 == FORCED_EMPTY] = EMPTY
    c2[c2 == FORCED_EMPTY] = EMPTY
    return (c1 == c2).all()

def rotate(grid):
    new = np.rot90(grid, 1).copy()
    
    # swap '/' and '\'
    # assume only frowns are in the grid
    new[new == Shape.leftFrown.value] = '🟢' # temp
    new[new == Shape.rightFrown.value] = Shape.leftFrown.value
    new[new == '🟢'] = Shape.rightFrown.value
    return new

@lru_cache()
def comb2(n, k):
    return comb(n, k)
    
def isShapeValueDiagonal(value, diagonal):
    global diagonals
    for shape in diagonals[diagonal]:
        if shape.value == value:
            return True
    
    return False

def relativeDirection(src, dest):
    """
    src and dest are absolute directions
    Given that you just went in direction src, return the relative direction that dest is in
    """
    newVal = (dest.value - src.value) % 8 + 1
    for direction in Direction:
        if direction.value == newVal:
            return direction
    
    raise ValueError(newVal)

def sortDownLeftLow(src, dest):
    """
    Helper function to sort that sorts clockwise starting with relative direction down left as the lowest value
    """
    direction = relativeDirection(src, dest)
    return (direction.value - Direction.downleft.value) % 8

class NextValue:
    def __init__(self, dx, dy, direction, diagonal):
        self.dx = dx
        self.dy = dy
        self.direction = direction
        self.diagonal = diagonal

class Solution:
    def __init__(self, n, wholeNumberArea):
        self.n = n
        self.wholeNumberArea = wholeNumberArea
        self.grid = np.full((self.n, self.n), EMPTY, dtype='<U2')
        self.sequence = np.zeros((self.n, self.n))
        self.numBoundary = 0
        self.numSolns = 0
        self.numIts = 0
        self.solns = []
        
    def __str__(self):
        return str(self.grid)
            
    def isEmpty(self, i, j):
        return self.grid[i,j] == EMPTY
                
    def isValid(self, i, j):
        shape = self.grid.shape
        return 0 <= i < shape[0] and 0 <= j < shape[1]
    
    def isCollisionSquare(self, i, j, dx, dy, diagonal):
        """
        Check if next value is already filled in with correct diagonal
        """
        to = (i + dy, j + dx)
        if to == (self.firstI, self.firstJ):
            return False
        
        return self.isValid(to[0], to[1]) and isShapeValueDiagonal(self.grid[to], diagonal)
    
    def isCollision(self, i, j, nextValues):
        for value in nextValues:
            if self.isCollisionSquare(i, j, value.dx, value.dy, value.diagonal):
                return True
            
        return False
        
    def nextValues(self, diagonal, direction):
        if diagonal == '/':
            if direction in (Direction.up, Direction.right, Direction.upright):
                return [NextValue(0, -1, Direction.up, '\\'),
                        NextValue(1, -1, Direction.upright, '/'),
                        NextValue(1, 0, Direction.right, '\\')]
            else:
                return [NextValue(-1, 0, Direction.left, '\\'),
                        NextValue(-1, 1, Direction.downleft, '/'),
                        NextValue(0, 1, Direction.down, '\\')]
        elif diagonal == '\\':
            if direction in (Direction.up, Direction.left, Direction.upleft):
                return [NextValue(0, -1, Direction.up, '/'),
                        NextValue(-1, -1, Direction.upleft, '\\'),
                        NextValue(-1, 0, Direction.left, '/')]
            else:
                return [NextValue(1, 0, Direction.right, '/'),
                        NextValue(1, 1, Direction.downright, '\\'),
                        NextValue(0, 1, Direction.down, '/')]
        else:
            raise ValueError(diagonal)
    
    def findOutsideHelper(self, i, j, grid2, outside):
        def isValid2(i, j):
            return 0 <= i < grid2.shape[0] and 0 <= j < grid2.shape[1]
        
        if not isValid2(i, j):
            return
        if outside[i,j] != 0:
            return
        if grid2[i,j] not in (EMPTY, FORCED_EMPTY):
            outside[i,j] = 0.5 # boundary
            return
        outside[i,j] = 1
        self.findOutsideHelper(i + 1, j, grid2, outside)
        self.findOutsideHelper(i - 1, j, grid2, outside)
        self.findOutsideHelper(i, j + 1, grid2, outside)
        self.findOutsideHelper(i, j - 1, grid2, outside)
        
        # check for diagonal boundaries
        if isValid2(i + 1, j + 1) and not grid2[i,j+1] == grid2[i+1,j] == Shape.leftFrown.value:
            # this is not a boundary, grid2[i+1,j+1] is still outside
            self.findOutsideHelper(i + 1, j + 1, grid2, outside)
        if isValid2(i + 1, j - 1) and not grid2[i,j-1] == grid2[i+1,j] == Shape.rightFrown.value:
            self.findOutsideHelper(i + 1, j - 1, grid2, outside)
        if isValid2(i - 1, j + 1) and not grid2[i,j+1] == grid2[i-1,j] == Shape.rightFrown.value:
            self.findOutsideHelper(i - 1, j + 1, grid2, outside)
        if isValid2(i - 1, j - 1) and not grid2[i,j-1] == grid2[i-1,j] == Shape.leftFrown.value:
            self.findOutsideHelper(i - 1, j - 1, grid2, outside)
        
    def findOutside(self):
        # add padding so that all outside squares are connected together
        grid2 = np.full((self.n + 2, self.n + 2), EMPTY, dtype='<U2')
        grid2[1:-1,1:-1] = self.grid
        outside = np.zeros_like(grid2, dtype="double")
        self.findOutsideHelper(0, 0, grid2, outside)
        
        # need to do this cuz part of boundary can be inside outer layer of boundary and we don't detect it
        outside[(grid2 != EMPTY) & (grid2 != FORCED_EMPTY)] = 0.5
        r = outside[1:-1,1:-1].copy() # return this
        
        # validation
        # make sure only one other island of 0s exist (at most)
        numIslands = 1 # outside
        for i in range(outside.shape[0]):
            for j in range(outside.shape[1]):
                if outside[i,j] == 0: # this should be the inside
                    self.findOutsideHelper(i, j, grid2, outside)
                    numIslands += 1
                    
        if numIslands > 2:
            print(numIslands)
            print(self)
            print(r)
            raise RuntimeError()
        return r

    def calculateArea2(self, allQuarts=False):
        """
        If allQuarts == True, assume each square on the boundary is a quarter
        Else assume half are quarts and half are slivers to get an integer area (must have even number of boundary points in this case)
        """
        outside = self.findOutside()
        numBoundary = (outside == 0.5).sum()
        numEmpty = (outside == 1).sum()
        assert(numBoundary % 2 == 0)
        area = self.grid.shape[0] * self.grid.shape[1] - numEmpty
        if allQuarts:
            area -= (1 - np.pi / 4) * numBoundary
            numQuarts = numBoundary
            numSlivers = 0
        else:
            area -= numBoundary // 2
            numQuarts = numSlivers = numBoundary // 2
        return area, numEmpty, numQuarts, numSlivers, outside
    
    # can combine with dfsShape but then becomes convoluted
    def longest(self, i, j, direction, diagonal):
        """
        Find the current longest area given an equal number of quarts and slivers
        Do this by trying to move as down left (relatively) as you can
        Can be thought of as rolling a ball from the current position as left as you can until you reach the top left corner
        Return False if no path exists
        """
        global diagonals
        found = False
        area = 0
        
        if (i,j) == (self.firstI, self.firstJ) and not self.isEmpty(i,j):
            if not isShapeValueDiagonal(self.grid[i,j], diagonal):
                return False, 0
            area = self.calculateArea2() # TODO: make sure don't need true argument
            return True, area[0]
        if not self.isValid(i, j):
            return False, 0
        if not self.isEmpty(i, j):
            return False, 0
                                   
        for shape in diagonals[diagonal]:
            self.grid[i,j] = shape.value
            nextValues = self.nextValues(diagonal, direction)
            nextValues.sort(key=lambda x: sortDownLeftLow(direction, x.direction))
            
            if self.isCollision(i, j, nextValues):
                break            
            for value in nextValues:
                found, area = self.longest(i + value.dy, j + value.dx, value.direction, value.diagonal)
                if found:
                    break
            
            if found:
                break
            break # TODO: Remove when accounting for sliv vs quart
        
        self.grid[i,j] = EMPTY
                
        return found, area
    
    # return False if too short (early stopping)
    # if trying to find longest: return True, area if possible, else False, 0
    # unused for now (combines dfsShape and longest functions)
    def dfsShape2(self, i, j, direction, diagonal, longest=False):
        def converter(normRet, longestRet, area):
            if longest:
                return longestRet, area
            return normRet
            
        global diagonals
        debug = DEBUG and not longest
        found = False
        area = 0
        
        if (i,j) == (self.firstI, self.firstJ) and not self.isEmpty(i,j):
            if not isShapeValueDiagonal(self.grid[i,j], diagonal):
                return converter(True, False, 0)

            area = self.calculateArea2() # TODOL make sure don't need True argument if longest
            if longest:
                return True, area[0]
            
            if area[0] == self.wholeNumberArea:
                print("VALID SOLUTION")
                outside = area[4]
                #print(outside)
                print(f"{self}\n{self.sequence}\n{area[:-1]}")
                self.numSolns += comb2(self.numBoundary, self.numBoundary // 2)
                
                toCopy = self.grid.copy()
                self.solns.append(toCopy)
            return True
        if not self.isValid(i, j):
            if debug:
                print("INVALID")
            return converter(True, False, 0)
        if not self.isEmpty(i, j):
            if debug:
                print("ALREADY FILLED")
            return converter(True, False, 0)
        if not longest:
            # find longest path
            found, area = self.dfsShape2(i, j, direction, diagonal, True)
            if not found:
                if debug:
                    print("IMPOSSIBLE")
                return True
            if area < self.wholeNumberArea:
                if debug:
                    print("TOO SHORT")
                return False
                                   
        self.numBoundary += 1
        self.sequence[i,j] = self.numBoundary
        if not longest:
            self.numIts += 1
        for shape in diagonals[diagonal]:
            self.grid[i,j] = shape.value
            nextValues = self.nextValues(diagonal, direction)
            nextValues.sort(key=lambda x: sortDownLeftLow(direction, x.direction))
            
            if self.isCollision(i, j, nextValues):
                if DEBUG:
                    print("COLLISION")
                break
            for value in nextValues:
                if not longest and (debug or self.numIts % 200000 == 0):
                    print(f"iter {self.numIts} at ({i},{j}) to ({i + value.dy},{j + value.dx} going direction {value.direction.name} {value.diagonal})")
                    input(self) if debug else print(self)                    
                r = self.dfsShape2(i + value.dy, j + value.dx, value.direction, value.diagonal, longest)
                if longest:
                    found, area = r
                    if found:
                        break
                elif not r:
                    break # too short, remaining paths will all be shorter
            if longest and found:
                break
            break # TODO: Remove when accounting for sliv vs quart
        
        self.grid[i,j] = EMPTY
        self.sequence[i,j] = 0
        self.numBoundary -= 1
        
        if debug:
            print("BACKTRACE")
        
        return converter(True, found, area)
    
    # return False if too short (early stopping)
    def dfsShape(self, i, j, direction, diagonal):
        global diagonals
        if (i,j) == (self.firstI, self.firstJ) and not self.isEmpty(i,j):
            if not isShapeValueDiagonal(self.grid[i,j], diagonal):
                return True

            area = self.calculateArea2()
            if area[0] == self.wholeNumberArea:
                print("VALID SOLUTION")
                outside = area[4]
                #print(outside)
                print(f"{self}\n{self.sequence}\n{area[:-1]}")
                self.numSolns += comb2(self.numBoundary, self.numBoundary // 2)
                
                toCopy = self.grid.copy()
                self.solns.append(toCopy)
            return True
        if not self.isValid(i, j):
            if DEBUG:
                print("INVALID")
            return True
        if not self.isEmpty(i, j):
            if DEBUG:
                print("ALREADY FILLED")
            return True
        found, area = self.longest(i, j, direction, diagonal)
        if not found:
            if DEBUG:
                print("IMPOSSIBLE")
            return True
        if area < self.wholeNumberArea:
            if DEBUG:
                print("TOO SHORT")
            return False
                                   
        self.numBoundary += 1
        self.sequence[i,j] = self.numBoundary
        self.numIts += 1
        for shape in diagonals[diagonal]:
            self.grid[i,j] = shape.value
            nextValues = self.nextValues(diagonal, direction)
            nextValues.sort(key=lambda x: sortDownLeftLow(direction, x.direction))
            
            if self.isCollision(i, j, nextValues):
                if DEBUG:
                    print("COLLISION")
                break
            for value in nextValues:
                if DEBUG or self.numIts % 200000 == 0:
                    print(f"iter {self.numIts} at ({i},{j}) to ({i + value.dy},{j + value.dx} going direction {value.direction.name} {value.diagonal})")
                    input(self) if DEBUG else print(self)                    
                if not self.dfsShape(i + value.dy, j + value.dx, value.direction, value.diagonal):
                    break # too short, remaining paths will all be shorter
            break # TODO: Remove when accounting for sliv vs quart
        
        self.grid[i,j] = EMPTY
        self.sequence[i,j] = 0
        self.numBoundary -= 1
        
        if DEBUG:
            print("BACKTRACE")
        
        return True
        
    def findTopLeft(self):
        prevNumSolns = 0
        numSolns = np.zeros_like(self.grid, dtype=int)
        for i in range(self.n):
            for j in range(self.n):
                self.firstI = i
                self.firstJ = j
                c = self.n - 1
                    
                # top left must be '/' going right
                self.dfsShape(self.firstI, self.firstJ, Direction.right, '/')
                                
                self.grid[i,j] = FORCED_EMPTY # this square is not the top left, must be empty
                numSolns[i,j] = self.numSolns - prevNumSolns
                prevNumSolns = self.numSolns
        
        return numSolns
    
    def solve(self):
        return self.findTopLeft()
    
if __name__ == "__main__":
    n = 7
    wholeNumberArea = 32
    s = Solution(n, wholeNumberArea)
    t = time.time()
    numSolns = s.solve()
    t = time.time() - t
    print(f"Solved in {int(t // 60)}:{t % 60}") 
    print(numSolns)
    assert(numSolns.sum() == s.numSolns)
    print(s.numSolns)
    print(f"its: {s.numIts}")
    
    # validation
    for sol in s.solns:
        r = sol
        # check if each rotation exists in the solution
        for i in range(3):
            r = rotate(r)
            found = False
            for sol in s.solns:
                if eqGrid(r, sol):
                    found = True
                    break
            if not found:
                print("Couldn't find:")
                print(r)
                raise RuntimeError()
