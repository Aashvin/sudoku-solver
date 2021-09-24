import sys
import math
from copy import deepcopy
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class Solver:

    def initial_setup(self, board):
        """
        Replace all the blank slots with sets containing all possible numbers (1-9)
        """
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == ".": board[i][j] = set(i for i in range(1, 10))


    def check_equal_boards(self, board1, board2):
        """
        Checks if two boards have the same values in each grid location
        """

        if board1 is None or board2 is None:
            return False

        for i in range(len(board1)):
            for j in range(len(board1[i])):
                if board1[i][j] != board2[i][j]: return False

        return True


    def get_new_set(self, board, i, j):
        """
        Calculates the new set of possible values for the specified grid location
        Does this by checking the rows, columns, and big boxes to eliminate values already there
        """

        new_set = set()

        # Check rows
        for item in board[i]:
            if not isinstance(item, set): new_set.add(item)

        # Check cols
        for row in range(len(board)):
            if not isinstance(board[row][j], set): new_set.add(board[row][j])

        # Check boxes
        bigbox_i = math.ceil((i + 1) / 3)
        bigbox_j = math.ceil((j + 1) / 3)
        for row in range(bigbox_i * 3 - 3, bigbox_i * 3):
            for column in range(bigbox_j * 3 - 3, bigbox_j * 3):
                if not isinstance(board[row][column], set): new_set.add(board[row][column])

        return set(str(row) for row in range(1, 10)).difference(new_set)



    def reduce_board(self, board):
        """
        Reduces the board by making new sets for each grid location
        Replaces sets of size 1 with the value that set contains
        Does this until there have been no reductions in comparison to the previous state
        """

        old_board = None
        while not self.check_equal_boards(board, old_board):
            old_board = deepcopy(board)
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if isinstance(board[i][j], set):
                        new_set = self.get_new_set(board, i, j)
                        if len(new_set) == 1: board[i][j] = new_set.pop()
                        elif len(new_set) == 0: return False
                        else: board[i][j] = new_set

        return True


    def check_board(self, board):
        """
        Checks the board and returns whether it has been solved or not by checking if there are any sets remaining
        """

        for i in board:
            for j in i:
                if isinstance(j, set): return False
            
        return True

    def find_shortest_set(self, board):
        """
        Finds the set with the least numbers in it for a higher chance at less iterations of backtracks
        """

        lowest = 9
        coords = (9, 9)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if isinstance(board[i][j], set) and len(board[i][j]) < lowest:
                    lowest = len(board[i][j])
                    coords = (i, j)

        return coords

    def solve(self, board):
        """
        The recursive function that is called until the board is solved or deemed unsolvable
        Handles the backtracking aspect if the current state of the board is unsolvable
        """

        # Checks if the reduction has changed anything and returns the board if nothing has changed
        old_board = deepcopy(board)
        if not self.reduce_board(board):
            return old_board
        
        # Checks if the board has been solved and returns the board if it has
        if self.check_board(board):
            return board

        shortest = self.find_shortest_set(board)

        # Make a copy of the current smallest set as a temporary to try
        temp_set = deepcopy(board[shortest[0]][shortest[1]])

        # While the board still hasn't been solved, pop an element from the smallest set and try solving from that state
        while not self.check_board(board):
            if len(temp_set) > 0:
                board[shortest[0]][shortest[1]] = temp_set.pop()
            else:
                # If the temp set contains no more options, the board is set to its state before attempting that set to backtrack
                board = deepcopy(old_board)
                break

            board = self.solve(board)

        return board

    def read_file(self):
        """
        Opens a window to select the file for the puzzle
        """

        Tk().withdraw()
        file_path = askopenfilename()
        
        f = open(file_path, "r")
        puzzle = f.readline()
        board = []
        for i in range(0, 9):
            row = []
            for j in range(0, 9):
                row.append(puzzle[i * 9 + j])
            board.append(row)

        return board

    def solveSudoku(self):
        """
        The main overarching function to run the solver
        """

        board = self.read_file()
        self.initial_setup(board)
        board = self.solve(board)

        for i in board:
            print(i)
        print(self.check_board(board))



solution = Solver()
solution.solveSudoku()