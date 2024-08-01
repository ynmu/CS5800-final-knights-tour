class KnightsTour:
    def __init__(self, rows=8, cols=8, startRow=0, startCol=0):
        '''
        The constructor initializes the board size and the
        possible moves for the knight

        rows: int, the number of rows of the board
        cols: int, the number of columns of the board
        startRow: int, indicating the starting row of the knight
        startCol: int, indicating the starting column of the knight
        '''
        self.possibleMoves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        self.rows = rows
        self.cols = cols
        self.board = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.board[startRow][startCol] = 0
        self.startRow = startRow
        self.startCol = startCol
        # Store the moves made by the knight, used for visualization
        self.moves = [(startRow, startCol, 0)]
        # Store the solution status, used for printing the solution
        self.solutionFound = None

    def getMoves(self):
        '''
        Get the moves made by the knight
        '''
        return self.moves

    def getBoard(self):
        '''
        Get a deep copy of the board
        '''
        return [row[:] for row in self.board]

    def solve(self):
        '''
        Solve the knight's tour problem, updating the board and moves
        '''
        step = 1
        if self._solveUtil(self.board, self.startRow, self.startCol, step):
            self.solutionFound = True
            return self.board
        else:
            self.solutionFound = False
            return None

    def printSolution(self):
        '''
        Print the solution of the knight's tour problem
        Only prints valid information after the solve() method is called
        '''
        if self.solutionFound is None:
            print('Problem not solved yet, call the solve() method first')
        elif self.solutionFound is False:
            print(f'No solution found for {self.rows}x{self.cols} board, '
                  f'starting from row {self.startRow}, column {self.startCol}')
        else:
            for row in self.board:
                print(' '.join(str(cell) for cell in row))

    def _canMove(self, x, y, board):
        '''
        Check if the knight can move to cell x, y
        (x, y) is valid if it is inside the board and the cell is not visited
        '''
        return 0 <= x < self.rows and 0 <= y < self.cols and board[x][y] == -1

    def _solveUtil(self, board, currRow, currCol, step):
        '''
        The recursive utility function to solve the knight's tour problem
        '''
        if step == self.rows * self.cols:
            return True

        # Try all possible moves from the current coordinate R, C
        for moveRow, moveCol in self.possibleMoves:
            newRow, newCol = currRow + moveRow, currCol + moveCol
            # if the new move is valid
            # mark the cell as visited and continue searching
            if self._canMove(newRow, newCol, board):
                board[newRow][newCol] = step
                self.moves.append((newRow, newCol, step))

                # Recursively look for solutions from the new move
                if self._solveUtil(board, newRow, newCol, step + 1):
                    return True

                # Backtrack if no solution is found
                board[newRow][newCol] = -1
                self.moves.append((newRow, newCol, -1))
        return False


if __name__ == '__main__':
    kt = KnightsTour(3, 4, 0, 0)
    chessboard = kt.solve()
    kt.printSolution()
