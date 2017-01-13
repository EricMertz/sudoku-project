#sudokutester.py
import pprint
import time
import sys

execfile("SudokuStarter.py")
sb = init_board("input_puzzles/easy/4_4.sudoku")
#sb = init_board("input_puzzles/more/9x9/9x9.1.sudoku")
#sb = init_board("input_puzzles/more/25x25/25x25.1.sudoku")
#sb = init_board("input_puzzles/more/9x9/9x9.1.sudoku")
sb.print_board()

omg = initialize(sb)
#pprint.pprint(omg)

#sb = init_board("input_puzzles/easy/9_9.sudoku")
#sb.print_board()

#omg = initialize(sb)
#pprint.pprint(omg)

"""result = consistent_move(omg, 2, 0, 4, 4) 
print result, ", should return false"

result = consistent_move(omg, 2, 0, 3, 4) 
print result, ", should return false"

result = consistent_move(omg, 2, 0, 2, 4) 
print result, ", should return true"

result = consistent_move(omg, 2, 0, 1, 4) 
print result, ", should return false"


result = consistent_move(omg, 2, 3, 1, 4) 
print result, ", should return true"


result = consistent_move(omg, 3, 1, 1, 4) 
print result, ", should return true"

result = consistent_move(omg, 1, 1, 4, 4) 
print result, ", should return true"

result = consistent_move(omg, 1, 1, 1, 4) 
print result, ", should return false"""


#apple = Move(1,2,3)
#print apple



#print LCV(omg, 4, 4, 9)
#print Degree(omg,4,4,9)

#worked, board = backtrackLCV(sb, omg)
#print worked
#board.print_board()

worked, board = solve(sb)
board.print_board()
print "regular ^^"

"""worked, board = solve(sb, LCV = True, forward_checking = False)
#board.print_board()
print "LCV ^^"
#time.sleep(10)

worked, board = solve(sb, Degree = True, forward_checking = False)
#board.print_board()
print "Degree ^^"
#time.sleep(10)

worked, board = solve(sb, MRV = True, forward_checking = False)
#board.print_board()
print "MRV ^^"
#time.sleep(10)

worked, board = solve(sb, LCV = True, forward_checking = True)
#board.print_board()
print "LCVFC ^^"
#time.sleep(10)

worked, board = solve(sb, Degree = True, forward_checking = True)
#board.print_board()
print "DegreeFC ^^"
#time.sleep(10)

worked, board = solve(sb, MRV = True, forward_checking = True)
#board.print_board()
print "MRVFC ^^"
#time.sleep(10)

worked, board = solve(sb, forward_checking = True)
#board.print_board()
print "FC ^^"
#time.sleep(10)

worked, board = solve(sb)
#board.print_board()
print "regular ^^"
#time.sleep(10)"""


