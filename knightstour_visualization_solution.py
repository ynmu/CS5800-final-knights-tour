import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from knightstour import KnightsTour
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import sys
import tkinter as tk
from tkinter import messagebox


class InputDialog:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Knight's Tour Input")
        self.window.geometry("300x400")
        self.window.grab_set()

        # Row input
        tk.Label(self.window, text="Number of rows:").pack(pady=5)
        self.row_spinbox = tk.Spinbox(self.window, from_=1, to=8, width=5)
        self.row_spinbox.pack(pady=5)

        # Column input
        tk.Label(self.window, text="Number of columns:").pack(pady=5)
        self.col_spinbox = tk.Spinbox(self.window, from_=1, to=8, width=5)
        self.col_spinbox.pack(pady=5)

        # Starting row input
        tk.Label(self.window, text="Starting row (0-indexed):").pack(pady=5)
        self.start_row_spinbox = tk.Spinbox(self.window, from_=0, to=8, width=5)
        self.start_row_spinbox.pack(pady=5)

        # Starting column input
        tk.Label(self.window, text="Starting column (0-indexed):").pack(pady=5)
        self.start_col_spinbox = tk.Spinbox(self.window, from_=0, to=8, width=5)
        self.start_col_spinbox.pack(pady=5)

        # Confirm button
        tk.Button(self.window, text="Confirm", command=self.confirm).pack(pady=10)

        # Initialize result
        self.result = None

    def confirm(self):
        # Retrieve values from spinboxes
        rows = int(self.row_spinbox.get())
        cols = int(self.col_spinbox.get())
        start_row = int(self.start_row_spinbox.get())
        start_col = int(self.start_col_spinbox.get())

        # Validate starting position
        if start_row < rows and start_col < cols:
            self.result = (rows, cols, start_row, start_col)
            self.window.destroy()
        else:
            messagebox.showerror("Invalid Input", "Starting position must be within board dimensions.")

    def get_result(self):
        return self.result


class KTVisualization:
    def __init__(self, rows, cols, start_row, start_col):
        self.rows = rows
        self.cols = cols
        self.start_row = start_row
        self.start_col = start_col
        self.CHESS_PIECE_IMG = 'knight.png'
        self.BROWN = '#b08974'
        self.BEIGE = '#ede7df'
        self.step = 0
        self.chessboard = np.full((self.rows, self.cols), -1)
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.texts = None
        self.remove_symbols = None
        self.imagebox = None
        self.moves = None

        self.init_board()

    def init_board(self):
        self.ax.set_xlim(0, self.cols)
        self.ax.set_ylim(0, self.rows)
        self.ax.set_xticks(np.arange(self.cols))
        self.ax.set_yticks(np.arange(self.rows))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.invert_yaxis()
        self.ax.xaxis.set_ticks_position('none')
        self.ax.yaxis.set_ticks_position('none')

        # Draw the squares with alternating colors
        for i in range(self.rows):
            for j in range(self.cols):
                color = self.BROWN if (i + j) % 2 == 0 else self.BEIGE
                rect = plt.Rectangle((j, i), 1, 1, facecolor=color)
                self.ax.add_patch(rect)

        # Label the rows and columns of the chessboard
        for i in range(self.rows):
            self.ax.text(
                -0.3, i + 0.5,
                str(self.rows - i),
                ha='center', va='center',
                fontsize=24, color='black',
                font='Arial'
            )
        for j in range(self.cols):
            self.ax.text(
                j + 0.5, -0.3,
                chr(65 + j),
                ha='center', va='center',
                fontsize=24, color='black',
                font='Arial'
            )

        plt.gca().set_aspect('equal', adjustable='box')

        self.init_texts()
        self.init_remove_symbols()

    def init_texts(self):
        # Initialize the number display in each cell (empty at the beginning)
        self.texts = [
            [
                self.ax.text(
                    j + 0.5, i + 0.5,
                    '',
                    ha='center', va='center',
                    fontsize=24, color='black',
                    font='Arial', weight='bold'
                )
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]

    def init_remove_symbols(self):
        self.remove_symbols = [
            [
                self.ax.text(
                    j + 0.5, i + 0.5,
                    '',
                    ha='center', va='center',
                    fontsize=50, color='#db382a',
                    font='Arial', weight='ultralight'
                )
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]

    def update(self, moves):
        self.chessboard.fill(-1)
        # Remove the existing imagebox if it exists
        for artist in self.ax.artists:
            artist.remove()

        for i in range(self.rows):
            for j in range(self.cols):
                self.texts[i][j].set_text('')

        for pos, (x, y) in enumerate(moves[:self.step]):
            # Show the chess piece
            if pos != -1:
                self.chessboard[x, y] = pos
                self.texts[x][y].set_text(str(pos))
                self.remove_symbols[x][y].set_text('')
                if pos == self.step - 1:
                    # Show the image
                    img = mpimg.imread(self.CHESS_PIECE_IMG)
                    self.imagebox = OffsetImage(img, zoom=0.12)
                    ab = AnnotationBbox(self.imagebox, (y + 0.5, x + 0.5),
                                        frameon=False)
                    self.ax.add_artist(ab)
                    # Adjust the style and position of text to match the image
                    self.texts[x][y].set_color('white')
                    self.texts[x][y].set_zorder(10)
                    self.texts[x][y].set_position((y + 0.47, x + 0.66))
                else:
                    # Reset the style and position of text
                    self.texts[x][y].set_color('black')
                    self.texts[x][y].set_position((y + 0.5, x + 0.5))
            else:
                self.chessboard[x, y] = -1
                self.remove_symbols[x][y].set_text('x')
                self.remove_symbols[x][y].set_zorder(10)
        self.fig.canvas.draw_idle()

    def continue_step(self, e):
        if self.step < len(self.moves):
            self.step += 1
        self.update(self.moves)

    def reverse_step(self, e):
        if self.step > 0:
            self.step -= 1
        self.update(self.moves)

    def reset_step(self, e):
        self.step = 0
        self.update(self.moves)

    def quit_visual(self, e):
        plt.close()

    def update_moves_solution(self):
        kt = KnightsTour(self.rows, self.cols, self.start_row, self.start_col)
        solution_board = kt.solve()
        self.moves = [[0, 0] for _ in range(self.rows * self.cols)]
        if solution_board is not None:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.moves[solution_board[i][j]] = [i, j]
        else:
            sys.exit(f'No solution found for {self.rows}x{self.cols} board, '
                     f'starting from row {self.start_row}, column {self.start_col}')

    def visualize_solution(self):
        # Solve the knight's tour and store moves
        self.update_moves_solution()

        # Add continue button
        axcontinue = plt.axes([0.25, 0.05, 0.15, 0.075])
        bcontinue = Button(axcontinue, 'Continue')
        bcontinue.on_clicked(self.continue_step)

        # Add reset button
        axreverse = plt.axes([0.45, 0.05, 0.15, 0.075])
        breverse = Button(axreverse, 'Reset')
        breverse.on_clicked(self.reset_step)

        # Add option to quit
        axquit = plt.axes([0.65, 0.05, 0.15, 0.075])
        bquit = Button(axquit, 'Quit')
        bquit.on_clicked(self.quit_visual)

        # Display the animation
        plt.show()


if __name__ == '__main__':
    # create main tkinter window
    root = tk.Tk()
    root.withdraw()  # hide the root window

    dialog = InputDialog(root)

    # Wait for the user to input the data and get the result
    root.wait_window(dialog.window)
    input_data = dialog.get_result()

    # Check if the user canceled the input dialog
    if input_data:
        rows, cols, start_row, start_col = input_data
        # Initialize and run the visualization
        kt_visual = KTVisualization(rows, cols, start_row, start_col)
        # Set `process=True` if you want to visualize the process with backtracking
        kt_visual.visualize(process=False)
    else:
        print("Input was canceled or invalid.")