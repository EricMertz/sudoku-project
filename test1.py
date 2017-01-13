#test1.py

execfile("SudokuStarter_blah.py")
sb = init_board("input_puzzles/more/25x25/25x25.1.sudoku")
initialize(sb)
sb.print_board()
worked, board = solve(sb, MRV = True, forward_checking = True )
board.print_board()