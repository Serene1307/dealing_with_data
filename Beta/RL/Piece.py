from enum import Enum

# https://en.wikipedia.org/wiki/Box-drawing_character
class Piece(Enum):
    CURVE_DOWN_RIGHT = '╭' # ╭ U+256D
    CURVE_DOWN_LEFT  = '╮' # ╮ U+256E
    CURVE_UP_LEFT    = '╯' # ╯ U+256F
    CURVE_UP_RIGHT   = '╰' # ╰ U+2570
    CROSS            = '┼' # ┼ U+253C
    TEE_RIGHT = '├' # ├ U+251C
    TEE_DOWN  = '┬' # ┬ U+252C 
    TEE_LEFT  = '┤' # ┤ U+2524
    TEE_UP    = '┴' # ┴ U+2534
    HORIZONTAL = '─'
    VERTICAL = '│'
    
    def rotate(self):
        if self is Piece.CURVE_DOWN_RIGHT:
            return Piece.CURVE_DOWN_LEFT
        if self is Piece.CURVE_DOWN_LEFT:
            return Piece.CURVE_UP_LEFT
        if self is Piece.CURVE_UP_LEFT:
            return Piece.CURVE_UP_RIGHT
        if self is Piece.CURVE_UP_RIGHT:
            return Piece.CURVE_DOWN_RIGHT
            
        if self is Piece.CROSS:
            return Piece.CROSS
        
        if self is Piece.TEE_RIGHT:
            return Piece.TEE_DOWN
        if self is Piece.TEE_DOWN:
            return Piece.TEE_LEFT
        if self is Piece.TEE_LEFT:
            return Piece.TEE_UP
        if self is Piece.TEE_UP:
            return Piece.TEE_RIGHT
        
        if self is Piece.HORIZONTAL:
            return Piece.VERTICAL
        if self is Piece.VERTICAL:
            return Piece.HORIZONTAL
   
    def equivalent(self):
        if self is Piece.CURVE_DOWN_RIGHT or self is Piece.CURVE_DOWN_LEFT or self is Piece.CURVE_UP_LEFT or self is Piece.CURVE_UP_RIGHT:
            return [Piece.CURVE_DOWN_RIGHT, Piece.CURVE_DOWN_LEFT, Piece.CURVE_UP_LEFT, Piece.CURVE_UP_RIGHT]
        
        if self is Piece.CROSS:
            return [Piece.CROSS]
        
        if self is Piece.TEE_RIGHT or self is Piece.TEE_DOWN or self is Piece.TEE_LEFT or self is Piece.TEE_UP:
            return [Piece.TEE_RIGHT, Piece.TEE_DOWN, Piece.TEE_LEFT, Piece.TEE_UP]
        
        if self is Piece.HORIZONTAL or self is Piece.VERTICAL:
            return [Piece.HORIZONTAL, Piece.VERTICAL]
        
    def canonical(self):
        if self is Piece.CURVE_DOWN_RIGHT or self is Piece.CURVE_DOWN_LEFT or self is Piece.CURVE_UP_LEFT or self is Piece.CURVE_UP_RIGHT:
            return Piece.CURVE_DOWN_RIGHT
        
        if self is Piece.CROSS:
            return Piece.CROSS
        
        if self is Piece.TEE_RIGHT or self is Piece.TEE_DOWN or self is Piece.TEE_LEFT or self is Piece.TEE_UP:
            return Piece.TEE_RIGHT
        
        if self is Piece.HORIZONTAL or self is Piece.VERTICAL:
            return Piece.VERTICAL
        
    def hasUp(self):
        if self is Piece.CURVE_UP_LEFT \
        or self is Piece.CURVE_UP_RIGHT \
        or self is Piece.CROSS \
        or self is Piece.TEE_RIGHT \
        or self is Piece.TEE_LEFT \
        or self is Piece.TEE_UP \
        or self is Piece.VERTICAL:
            return True
        else:
            return False
        
        
    def hasDown(self):
        if self is Piece.CURVE_DOWN_RIGHT \
        or self is Piece.CURVE_DOWN_LEFT \
        or self is Piece.CROSS \
        or self is Piece.VERTICAL \
        or self is Piece.TEE_RIGHT \
        or self is Piece.TEE_DOWN \
        or self is Piece.TEE_LEFT:
            return True
        else:
            return False
        
        
    def hasRight(self):
        if self is Piece.CURVE_DOWN_RIGHT \
        or self is Piece.CURVE_UP_RIGHT \
        or self is Piece.CROSS \
        or self is Piece.HORIZONTAL \
        or self is Piece.TEE_RIGHT \
        or self is Piece.TEE_DOWN \
        or self is Piece.TEE_UP:
            return True
        else:
            return False   
            
    def hasLeft(self):
        if self is Piece.CURVE_DOWN_LEFT \
        or self is Piece.CURVE_UP_LEFT \
        or self is Piece.CROSS \
        or self is Piece.HORIZONTAL \
        or self is Piece.TEE_LEFT \
        or self is Piece.TEE_DOWN \
        or self is Piece.TEE_UP:
            return True
        else:
            return False 
        
    def matchesRight(self, piece):
        if self.connectsRight(piece) or not self.hasRight() and not piece.hasLeft():
            return True
        else:
            return False
        
    def matchesLeft(self, piece):
        if self.connectsLeft(piece)  or not self.hasLeft() and not piece.hasRight():
            return True
        else:
            return False

       
    def matchesDown(self, piece):
        if self.connectsDown(piece) or not self.hasDown() and not piece.hasUp():
            return True
        else:
            return False
        
    def matchesUp(self, piece):
        if self.connectsUp(piece) or not self.hasUp() and not piece.hasDown():
            return True
        else:
            return False
        
    def connectsRight(self, piece):
        if self.hasRight() and piece.hasLeft():
            return True
        else:
            return False
        
    def connectsLeft(self, piece):
        if self.hasLeft() and piece.hasRight():
            return True
        else:
            return False

       
    def connectsDown(self, piece):
        if self.hasDown() and piece.hasUp():
            return True
        else:
            return False
        
    def connectsUp(self, piece):
        if self.hasUp() and piece.hasDown():
            return True
        else:
            return False        



    