#!/usr/bin/env python
import struct, string, math
from copy import *

"""class Move:
    def __init__(self, row, col, val):
        constructor for the Move
        self.Row = row
        self.Col = col
        self.Val = val

    def __str__ (self):
        return "row:"+ str(self.Row)+ " col:"+ str(self.Col)+ " val:"+ str(self.Val)

    def changeVal(self, val):
        self.Val = val"""

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
        """the constructor for the SudokuBoard"""
        self.BoardSize = size #the size of the board
        self.CurrentGameBoard= board #the current state of the game board

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
                                                                  
    #def __deepcopy__(self):
    #    deepcopy(self.CurrentGameBoard)
                                                                  
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def initializator(row, col, val, size, legals):
    #so if there is a 7 in 3,4 then we set the first element to 7 and the rest to 0
    subsquare = int(math.sqrt(size))
    legals[row][col][0] = val
    for i in range(1,size+1):
        legals[row][col][i] = 0

    #check for inconsistencies
    #sets rows and columns
    for i in range(size):
        legals[row][i][val] = 0 
        legals[i][col][val] = 0

    #sets box

    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            legals[SquareRow*subsquare+i][SquareCol*subsquare+j][val] = 0

    return legals

def initialize(initial_board):
    temp = deepcopy(initial_board)
    size = temp.BoardSize

    legals = [[[1 for i in range(size+1)] for j in range(size)] for k in range(size)]
    for i in range(size):
        for j in range(size):
            legals[i][j][0] = 0

    for i in range(size):
        for j in range(size):
            if temp.CurrentGameBoard[i][j] != 0:
                legals = initializator(i, j, temp.CurrentGameBoard[i][j], size, legals)
    return legals

def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    print "Your code will solve the initial_board here!"
    print "Remember to return the final board (the SudokuBoard object)."
    print "I'm simply returning initial_board for demonstration purposes."

    legals = initialize(initial_board)
    if forward_checking:
        return backtrackFC(initial_board, legals)
    elif MRV:
        return backtrackMRV(initial_board, legals)
    elif Degree:
        return backtrackDegree(initial_board, legals)
    elif LCV:
        return backtrackLCV(initial_board, legals)
    else:
        return backtrack(initial_board, legals)
    
    return False, initial_board


def backtrack(board, legals):
    if is_complete(board):
        return True, board
    size = board.BoardSize
    row, col = next_open_square(legals, size)
    #print row, col
    ls = order_domain_values(legals, row, col, size)
    for val in ls:
        if legals[row][col][val] == 1:
            new_board = SudokuBoard(size, deepcopy(board.CurrentGameBoard))
            new_board = new_board.set_value(row, col, val)
            newLegals, sent = make_3D_move(deepcopy(legals), row, col, val, size)
            worked, board = backtrack(new_board, newLegals)
            if worked:
                return True, board

    return False, board

def backtrackFC(board, legals):
    if is_complete(board):
        return True, board
    size = board.BoardSize
    row, col = MRV(legals, size)
    #print row, col
    ls = LCV(legals, row, col, size)
    for val in ls:
        if consistent_move(legals, row, col, val, size):
            new_board = SudokuBoard(size, deepcopy(board.CurrentGameBoard))
            new_board = new_board.set_value(row, col, val)
            newLegals, sent = make_3D_move(deepcopy(legals), row, col, val, size)
            worked, board = backtrack(new_board, newLegals)
            if worked:
                return True, board

    return False, board

def backtrackMRV(board, legals):
    if is_complete(board):
        return True, board
    size = board.BoardSize
    row, col = MRV(legals, size)
    #print row, col
    ls = order_domain_values(legals, row, col, size)
    for val in ls:
        if legals[row][col][val] == 1:
            new_board = SudokuBoard(size, deepcopy(board.CurrentGameBoard))
            new_board = new_board.set_value(row, col, val)
            newLegals, sent = make_3D_move(deepcopy(legals), row, col, val, size)
            worked, board = backtrack(new_board, newLegals)
            if worked:
                return True, board

    return False, board

def backtrackDegree(board, legals):
    if is_complete(board):
        return True, board
    size = board.BoardSize
    row, col = next_open_square(legals, size)
    #print row, col
    ls = order_domain_values(legals, row, col, size)
    for val in ls:
        if legals[row][col][val] == 1:
            new_board = SudokuBoard(size, deepcopy(board.CurrentGameBoard))
            new_board = new_board.set_value(row, col, val)
            newLegals, sent = make_3D_move(deepcopy(legals), row, col, val, size)
            worked, board = backtrack(new_board, newLegals)
            if worked:
                return True, board

    return False, board

def backtrackLCV(board, legals):
    if is_complete(board):
        return True, board
    size = board.BoardSize
    row, col = next_open_square(legals, size)
    #print row, col
    ls = LCV(legals, row, col, size)
    for val in ls:
        if legals[row][col][val] == 1:
            new_board = SudokuBoard(size, deepcopy(board.CurrentGameBoard))
            new_board = new_board.set_value(row, col, val)
            newLegals, sent = make_3D_move(deepcopy(legals), row, col, val, size)
            worked, board = backtrack(new_board, newLegals)
            if worked:
                return True, board

    return False, board

def next_open_square(legals, size):
    for i in range(size):
        for j in range(size):
            if legals[i][j][0] == 0:
                return i,j
def order_domain_values(legals, row, col, size):
    ls = []
    for i in range(1,(size+1)):
        if legals[row][col][i] == 1:
            ls.append(i)
    return ls

def make_3D_move(legals, row, col, val, size):
    legals[row][col][0] = val
    for i in range(1,(size+1)):
        legals[row][col][i] = 0
        legals[row][i-1][val] = 0
        legals[i-1][col][val] = 0
        if (sum(legals[row][col]) == 0 or sum(legals[row][i-1]) == 0 or sum(legals[i-1][col]) == 0):
            return legals, False

    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            legals[SquareRow*subsquare+i][SquareCol*subsquare+j][val] = 0 
            if (sum(legals[SquareRow*subsquare+i][SquareCol*subsquare+j]) == 0):
                return legals, False

    return legals, True

    
    
def consistent_move(legals, row, col, val, size):

    if legals[row][col][val] == 0:
        #print "this move cant be made"
        return False
    subsquare = int(math.sqrt(size))
    for i in range(size):
        if legals[i][col][0] != 0 and i != row:
            #print "this row is already full"
            continue 
        if legals[i][col][val] == 0 and i != row:
            #print "this row cant be that number!"
            continue
        if sum(legals[i][col][1:]) == 1 and i != row:
            #print "if this move is made, then there will be no other options for this row~!"
            return False

    for i in range(size):
        if legals[row][i][0] != 0 and i != col:
            #print "this col is already full"
            continue
        if legals[row][i][val] == 0 and i != col:
            #print "this col cant be that number!"
            continue
        if sum(legals[row][i][1:]) == 1 and i != col:
            #print "if this move is made, then there will be no other options for this col~!"
            return False

    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            if legals[SquareRow*subsquare+i][SquareCol*subsquare+j][0] == 0 and not(i == row and j == col):
                #print "this subsquare already has a number"
                continue
            if legals[SquareRow*subsquare+i][SquareCol*subsquare+j][val] == 0 and not(i == row and j == col):
                #print "this subsquare cant be that number"
                continue
            if sum(legals[SquareRow*subsquare+i][SquareCol*subsquare+j][1:]) == 1 and not(i == row and j == col):
                #print "if this move is made, then there will be no other options for this subsquare!~"
                return False
    return True



def MRV(legals, size):
    row = 0
    col = 0
    score = 1000
    for i in range(size):
        for j in range(size):
            if (legals[i][j][0] == 0):
                s = 0
                for k in range(1,(size+1)):
                    s += legals[i][j][k]
                if s < score:
                    row = i
                    col = j
                    score = s
    return (row, col)

def constraint_counter(legals, row, col, val, size):
    count_1 = 0
    for i in range(size):
        for j in range(size):
            for k in range(1, size+1):
                count_1 += legals[i][j][k]
    
    legals[row][col][0] = val
    for i in range(1,(size+1)):
        legals[row][col][i] = 0
        legals[row][i-1][val] = 0
        legals[i-1][col][val] = 0

    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            legals[SquareRow*subsquare+i][SquareCol*subsquare+j][val] = 0

    count_2 = 0
    for i in range(size):
        for j in range(size):
            for k in range(1, size+1):
                count_2 += legals[i][j][k]

    return count_1 - count_2

def LCV(legals, row, col, size):
    vals = []
    temp = deepcopy(legals)
    for i in range(1,(size+1)):
        if temp[row][col][i] == 1: 
            vals.append(i)

    constraintVals = []
    for num in vals:
        constraintVals.append(constraint_counter(temp, row, col, num, size))
    #print constraintVals, vals
    return [y for (x,y) in sorted(zip(constraintVals,vals))]

def Degree(legals, row, col, size):
    vals = []
    temp = deepcopy(legals)
    for i in range(1,(size+1)):
        if temp[row][col][i] == 1: 
            vals.append(i)

    constraintVals = []
    for num in vals:
        constraintVals.append(-(constraint_counter(temp, row, col, num, size)))
    #print constraintVals, vals
    return [y for (x,y) in sorted(zip(constraintVals,vals))]