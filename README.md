# Knight's Tour Visualization

This repo contains an implementation of the Knight's Tour algorithm, as well as visualization tools to illustrate the backtracking process and final solution of the algorithm.

## Features

### Knight's Tour Algorithm

- **Implementation:** The Knight's Tour algorithm is implemented and allows users to simulate the knight's path on a chessboard.
- **Initialization:** The tour can be initialized using `KnightsTour()`. The board size (rows and columns) and the starting position of the knight can be specified. By default, the board is 8x8, and the knight starts from the top-left corner.

### Visualization of Backtracking Process

- **Status:** Almost completed
- **Details:** The visualization demonstrates the backtracking process of the algorithm. The knight moves to the next available position. If no moves are possible, it backtracks until it finds a viable path forward. The current position of the knight is marked as "Knight."
- **Optimization:** To reduce computation time, the visualization is demonstrated on a smaller, fixed-size board of 4x3.
- **Future Enhancements** Consider replacing the "Knight" text with an image of a chess piece for better visual representation.

### Visualization of the Solution

- **Status:** To do
- **Objective:** This visualization will only show the solution path of the knight's tour. Unlike the backtracking visualization, it will not display the full backtracking process. Users can therefore specify the board size and starting position for this visualization, since there are no major concerns for the computing time.
