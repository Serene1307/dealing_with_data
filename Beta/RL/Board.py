from collections import Counter
import random
from copy import copy, deepcopy
import pickle

class Board(object):

    def __init__(self, pieces, rows, columns, board=None):
        """Copy an existing board."""
        self.pieces = pieces
        self.rows = rows
        self.columns = columns
        assert(len(pieces) == rows*columns)
        if board:
            self.board = deepcopy(board)
        else:
            self.board = [[None for i in range(self.columns)] for i in range(self.rows)]
            
        assert(len(self.board)==self.rows)
        assert(len(self.board[0])==self.columns)
            
        self._b1 = self.board
        self._b2 = None
        self._b3 = None
        self._b4 = None
        self.p = None
            
    def __eq__(self, other):
        
        if not self.p:
            self.__cache__() 
        
        if isinstance(other, self.__class__):
            return self._b1 == other._b1 \
                or self._b2 == other._b1 \
                or self._b3 == other._b1 \
                or self._b4 == other._b1
        return False
    
    def __hash__(self):
        
        if not self.p:
            self.__cache__() 
        
        return hash(self.p)
        
    def __cache__(self):
        self._b1 = self.board # trim()
        self._b2 = self.rotate().board # .trim()
        self._b3 = self.rotate().rotate().board # .trim().trim()
        self._b4 = self.rotate().rotate().rotate().board # .trim().trim()
        p1 = pickle.dumps(self._b1, -1)
        p2 = pickle.dumps(self._b2, -1)
        p3 = pickle.dumps(self._b3, -1)
        p4 = pickle.dumps(self._b4, -1)
        lst = sorted([hash(p1), hash(p2), hash(p3), hash(p4)])
        self.p = pickle.dumps(lst, -1)
        
    def placePiece(self, piece, i, j):
        result = Board(self.pieces, self.rows, self.columns, self.board)
        result.board[i][j]=piece
        return result
    
    def rotate(self):
        result = Board(self.pieces, self.columns, self.rows)
        rotated = list( zip(*self.board[::-1]) )
        for i in range(result.rows):
            for j in range(result.columns):
                if rotated[i][j]:
                    result.board[i][j] = rotated[i][j].rotate()

        return result
    
    def getBoard(self):
        return self.board # trim()
    
    def getLine(self, i):
        return self.board[i]
    
    def getColumn(self, i):
        return [self.board[k][i] for k in range(self.rows)]

    '''
    def trim(self):
        min_y=-1
        for i in range(self.rows):
            if not any(self.getLine(i)):
                min_y=i
            else:
                break

        max_y=self.rows
        for i in reversed(range(self.rows)):
            if not any(self.getLine(i)):
                max_y=i
            else:
                break
        
        min_x=-1
        for i in range(self.columns):
            if not any(self.getColumn(i)):
                min_x=i
            else:
                break

        max_x=self.columns
        for i in reversed(range(self.columns)):
            if not any(self.getColumn(i)):
                max_x=i
            else:
                break
                
        #print(min_x,min_y,max_x,max_y)
                
        return [[item for item in lst[min_x+1:max_x]] for lst in self.board[min_y+1:max_y]  ]
     '''   
        

    def countPlacedPieces(self):
        flat = [item.canonical().value for sublist in self.board for item in sublist if item != None]
        return Counter(flat)
    
    def getSize(self):
        flat = [item.canonical().value for sublist in self.board for item in sublist if item != None]
        return len(flat)
        
            
        
    def countGivenPieces(self):
        return Counter([item.canonical().value for item in self.pieces])
    
    def countAvailablePieces(self):
        given = self.countGivenPieces()
        placed = self.countPlacedPieces()
        given.subtract(placed)
        return given
    
    def printLine(line):
        return "".join([p.value if p!=None else '.' for p in line ])

    
    def printBoard(self):
        return "\n".join([Board.printLine(line) for line in self.board])
        

    def hasNeighborUp(self, i, j):
        if i-1>=0 and self.board[i-1][j]:
            return self.board[i-1][j]
        else:
            return None
        
    def hasNeighborDown(self, i, j):
        if i+1<self.rows and self.board[i+1][j]:
            return self.board[i+1][j]
        else:
            return None
        
    def hasNeighborLeft(self, i, j):
        if j-1>=0 and self.board[i][j-1]:
            return self.board[i][j-1]
        else:
            return None
        
    def hasNeighborRight(self, i, j):
        if j+1<self.columns and self.board[i][j+1]:
            return self.board[i][j+1]
        else:
            return None
        
    def validCell(self, piece, i, j):
        # Cell needs to be empty (None)
        if self.board[i][j]:
            return False
        
        # Cell needs to connect to all non-empty neighbors
        up = self.hasNeighborUp(i,j)
        if up:
            if not piece.matchesUp(up):
                return False
            else:
                connectsUp = piece.connectsUp(up)
           
        down = self.hasNeighborDown(i,j)
        if down:
            if not piece.matchesDown(down):
                return False
            else:
                connectsDown = piece.connectsDown(down)
        
        left = self.hasNeighborLeft(i, j)
        if left:
            if not piece.matchesLeft(left):
                return False
            else:
                connectsLeft = piece.connectsLeft(left)
        
        right = self.hasNeighborRight(i, j)
        if right:
            if not piece.matchesRight(right):
                return False
            else:
                connectsRight = piece.connectsRight(right)
        
        # The cell needs to have at least one neighbor
        # and need to be matched (if not)
        if up and connectsUp \
        or down and connectsDown \
        or left and connectsLeft \
        or right and connectsRight:
            return True
        else:
            return False
        
    
    def places(self, piece):
        if len(self.countPlacedPieces()) == 0:
            return [(0,0)]
        
        result = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.validCell(piece, i, j):
                    result.append((i,j))
        return result
    
    def getActions(self):
        result = []
        counter = current_board.countAvailablePieces()
        symbols = [item for item in counter.keys() if counter[item]>0]
        for symbol in symbols:
            for piece in Piece(symbol).equivalent():
                places = self.places(piece)
                for i,j in places:
                    action = (piece, i,j)
                    result.append( action )
        return result
    

    def containsNull(self):
        lol = self.board # .trim()trim()
        for l in lol:
            if not all(l):
                return True
        return False

    
    def getCellScore(self,i,j):
        p = self.board[i][j]
        if not p:
            return 0
        score = 0;
        if not self.hasNeighborUp(i,j) and p.hasUp():
            score += 1
        if not self.hasNeighborDown(i,j) and p.hasDown():
            score += 1
        if not self.hasNeighborRight(i,j) and p.hasRight():
            score += 1
        if not self.hasNeighborLeft(i,j) and p.hasLeft():
            score += 1
        return score

    
    def getScore(self):
        score = 0;
        for i in range(self.rows):
            for j in range(self.columns):
                score += self.getCellScore(i,j)
        return score
        

