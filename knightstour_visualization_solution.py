import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from knightstour import KnightsTour
import matplotlib.image as mpimg
import tkinter as tk
from tkinter import messagebox
from matplotlib.animation import FuncAnimation


class InputDialog:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Knight's Tour Input")
        self.window.geometry("300x400")
        self.window.grab_set()

        # Row input
        tk.Label(self.window, text="Number of rows:").pack(pady=5)
        # default to 3x4 board
        self.row_spinbox = tk.Spinbox(self.window, from_=1, to=8, width=5, value=3)
        self.row_spinbox.pack(pady=5)

        # Column input
        tk.Label(self.window, text="Number of columns:").pack(pady=5)
        self.col_spinbox = tk.Spinbox(self.window, from_=1, to=8, width=5, value=4)
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
        tk.Button(self.window, text="Confirm", command=self._confirm).pack(pady=10)

        # Initialize result
        self.result = None

    def _confirm(self):
        try:
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
                messagebox.showerror(
                    "Invalid Input",
                    "Starting position must be within board dimensions."
                )
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid integer values for all fields."
            )

    def get_result(self):
        return self.result


class KTVisualization:
    def __init__(self, rows, cols, start_row, start_col):
        self.CHESS_PIECE_IMG = 'knight.png'
        self.BROWN = '#b08974'
        self.BEIGE = '#ede7df'
        self.SIZE_MULTIPLIER = 1 / max(rows, cols)

        self.rows = rows
        self.cols = cols
        self.start_row = start_row
        self.start_col = start_col
        self.step = 0
        self.chessboard = np.full((self.rows, self.cols), -1)
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.texts = None
        self.remove_symbols = None
        self.imagebox = None
        self.moves = None

        self._init_board()

    def _init_board(self):
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
                fontsize=80 * self.SIZE_MULTIPLIER,
                color='black', weight='bold',
                font='Arial'
            )
        for j in range(self.cols):
            self.ax.text(
                j + 0.5, -0.3,
                chr(65 + j),
                ha='center', va='center',
                fontsize=80 * self.SIZE_MULTIPLIER,
                color='black', weight='bold',
                font='Arial'
            )

        plt.gca().set_aspect('equal', adjustable='box')

        self._init_texts()
        self._init_remove_symbols()

    def _init_texts(self):
        # Initialize the number display in each cell (empty at the beginning)
        self.texts = [
            [
                self.ax.text(
                    j + 0.5, i + 0.5,
                    '',
                    ha='center', va='center',
                    fontsize=80 * self.SIZE_MULTIPLIER,
                    color='black',
                    font='Arial', weight='bold'
                )
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]

    def _init_remove_symbols(self):
        self.remove_symbols = [
            [
                self.ax.text(
                    j + 0.5, i + 0.5,
                    '',
                    ha='center', va='center',
                    fontsize=200 * self.SIZE_MULTIPLIER,
                    color='#db382a',
                    font='Arial', weight='ultralight'
                )
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]

    def _update(self, moves):
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
                    start_pos = moves[self.step - 2] if self.step > 1 else (self.start_row, self.start_col)
                    self._show_motion(start_pos, (x, y))
                else:
                    # Reset the style and position of text
                    self.texts[x][y].set_color('black')
                    self.texts[x][y].set_position((y + 0.5, x + 0.5))
            else:
                self.chessboard[x, y] = -1
                self.remove_symbols[x][y].set_text('x')
                self.remove_symbols[x][y].set_zorder(10)
        self.fig.canvas.draw_idle()

    def _continue_step(self, e):
        if self.step < len(self.moves):
            self.step += 1
        else:
            return
        self._update(self.moves)

    def _reverse_step(self, e):
        if self.step > 0:
            self.step -= 1
        self._update(self.moves)

    def _reset_step(self, e):
        self.step = 0
        self._update(self.moves)

    def _quit_visual(self, e):
        plt.close()

    def _store_moves(self):
        kt = KnightsTour(self.rows, self.cols, self.start_row, self.start_col)
        solution_board = kt.solve()
        if solution_board is not None:
            self.moves = [(0, 0) for _ in range(self.rows * self.cols)]
            for i in range(self.rows):
                for j in range(self.cols):
                    self.moves[solution_board[i][j]] = (i, j)

    def _show_motion(self, start_pos, end_pos):
        # Load the checker piece image
        checker_img = mpimg.imread(self.CHESS_PIECE_IMG)
        imagebox = self.ax.imshow(checker_img, extent=[0, 1, 0, 1], origin='lower')

        # Animation function
        def animate(frame):
            x, y = frame
            imagebox.set_extent([x, x + 1, y, y + 1])
            return imagebox,

        # Create list of coordinates for animation
        steps = 20
        x_coords = np.linspace(start_pos[1], end_pos[1], steps)
        y_coords = np.linspace(start_pos[0], end_pos[0], steps)
        frames = list(zip(x_coords, y_coords))

        # Create the animation
        ani = FuncAnimation(self.fig, animate, frames=frames, interval=3, blit=True, repeat=False)

        plt.show()

    def visualize_solution(self):
        # Solve the knight's tour and store moves
        self._store_moves()
        if self.moves is None:
            messagebox.showerror(
                "No Solution",
                "No solution found for the given board."
            )
            return

        # Add continue button
        axcontinue = plt.axes([0.25, 0.05, 0.15, 0.075])
        bcontinue = Button(axcontinue, 'Continue')
        bcontinue.on_clicked(self._continue_step)

        # Add reset button
        axreverse = plt.axes([0.45, 0.05, 0.15, 0.075])
        breverse = Button(axreverse, 'Reset')
        breverse.on_clicked(self._reset_step)

        # Add option to quit
        axquit = plt.axes([0.65, 0.05, 0.15, 0.075])
        bquit = Button(axquit, 'Quit')
        bquit.on_clicked(self._quit_visual)

        # Display the animation
        plt.show()


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    dialog = InputDialog(root)

    # Wait for the user to input the data and get the result
    root.wait_window(dialog.window)
    input_data = dialog.get_result()

    # Check if the user canceled the input dialog
    if input_data:
        rows, cols, start_row, start_col = input_data
        # Initialize and run the visualization
        kt_visual = KTVisualization(rows, cols, start_row, start_col)
        kt_visual.visualize_solution()
    else:
        print("Input was canceled.")
