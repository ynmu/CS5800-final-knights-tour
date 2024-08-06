from knightstour_visualization_solution import KTVisualization
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from knightstour import KnightsTour
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


class KTVisualizationProcess(KTVisualization):
    def __init__(self, rows, cols, start_row, start_col):
        super().__init__(rows, cols, start_row, start_col)

    def _update(self, moves):
        self.chessboard.fill(-1)
        # Remove the existing imagebox if it exists
        for artist in self.ax.artists:
            artist.remove()

        for i in range(self.rows):
            for j in range(self.cols):
                self.texts[i][j].set_text('')

        for i, (x, y, pos) in enumerate(moves[:self.step]):
            # show the chess piece
            if pos != -1:
                self.chessboard[x, y] = pos
                self.texts[x][y].set_text(str(pos))
                self.remove_symbols[x][y].set_text('')
                if i == self.step - 1:
                    # show the image
                    img = mpimg.imread(self.CHESS_PIECE_IMG)
                    imagebox = OffsetImage(img, zoom=0.12)
                    ab = AnnotationBbox(imagebox, (y + 0.5, x + 0.5),
                                        frameon=False)
                    self.ax.add_artist(ab)
                    # adjust the style and position of text to match the image
                    self.texts[x][y].set_color('white')
                    self.texts[x][y].set_zorder(10)
                    self.texts[x][y].set_position((y + 0.47, x + 0.66))
                else:
                    # reset the style and position of text
                    self.texts[x][y].set_color('black')
                    self.texts[x][y].set_position((y + 0.5, x + 0.5))
            else:
                # reset the cell during backtracking
                self.chessboard[x, y] = -1
                self.remove_symbols[x][y].set_text('x')
                self.remove_symbols[x][y].set_zorder(10)
        self.fig.canvas.draw_idle()

    def _store_moves(self):
        kt = KnightsTour(self.rows, self.cols, self.start_row, self.start_col)
        kt.solve()
        self.moves = kt.getMoves()

    def _continue_step(self, e):
        if self.step < len(self.moves):
            self.step += 1
        self._update(self.moves)

    def visualize_process(self):
        # Solve the knight's tour and store moves
        self._store_moves()

        # Add continue button
        axcontinue = plt.axes([0.25, 0.05, 0.15, 0.075])
        bcontinue = Button(axcontinue, 'Continue')
        bcontinue.on_clicked(self._continue_step)

        # Add reverse button
        axreverse = plt.axes([0.45, 0.05, 0.15, 0.075])
        breverse = Button(axreverse, 'Reverse')
        breverse.on_clicked(self.reverse_step)

        # Add option to quit
        axquit = plt.axes([0.65, 0.05, 0.15, 0.075])
        bquit = Button(axquit, 'Quit')
        bquit.on_clicked(self.quit_visual)

        # Display the animation
        plt.show()


if __name__ == "__main__":
    rows, cols, start_row, start_col = 3, 4, 0, 0
    kt_visual = KTVisualizationProcess(rows, cols, start_row, start_col)
    kt_visual.visualize_process()
