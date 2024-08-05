import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from knightstour import KnightsTour
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


# The size of the board and the starting position of the knight
ROWS = 3
COLS = 4
START_ROW = 0
START_COL = 0

CHESS_PIECE_IMG = 'knight.png'
BROWN = '#b08974'
BEIGE = '#ede7df'

# global variables
step = 0
chessboard = np.full((ROWS, COLS), -1)
fig, ax = plt.subplots(figsize=(6, 6))

# Initialize the board
ax.set_xlim(0, COLS)
ax.set_ylim(0, ROWS)
ax.set_xticks(np.arange(COLS))
ax.set_yticks(np.arange(ROWS))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.invert_yaxis()
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# Draw the squares with alternating colors
for i in range(ROWS):
    for j in range(COLS):
        color = BROWN if (i + j) % 2 == 0 else BEIGE
        rect = plt.Rectangle((j, i), 1, 1, facecolor=color)
        ax.add_patch(rect)

# Label the rows and columns of the chessboard
for i in range(ROWS):
    ax.text(
        -0.3, i + 0.5,
        str(ROWS - i),
        ha='center', va='center',
        fontsize=24, color='black',
        font='Arial'
    )
for j in range(COLS):
    ax.text(
        j + 0.5, -0.3,
        chr(65 + j),
        ha='center', va='center',
        fontsize=24, color='black',
        font='Arial'
    )

plt.gca().set_aspect('equal', adjustable='box')

# Initialize the number display in each cell (empty at the beginning)
texts = [
    [
        ax.text(
            j + 0.5, i + 0.5,
            '',
            ha='center', va='center',
            fontsize=24, color='black',
            font='Arial', weight='bold'
        )
        for j in range(COLS)
    ]
    for i in range(ROWS)
]


remove_symbols = [
    [
        ax.text(
            j + 0.5, i + 0.5,
            '',
            ha='center', va='center',
            fontsize=50, color='#db382a',
            font='Arial', weight='ultralight'
        )
        for j in range(COLS)
    ]
    for i in range(ROWS)
]

# Store the image box for the knight piece
imagebox = None


# Update function for visualizing each step of the tour
def update():
    global imagebox
    chessboard.fill(-1)
    # Remove the existing imagebox if it exists
    for artist in ax.artists:
        artist.remove()

    for i in range(ROWS):
        for j in range(COLS):
            texts[i][j].set_text('')

    for i, (x, y, pos) in enumerate(moves[:step]):
        # show the chess piece
        if pos != -1:
            chessboard[x, y] = pos
            texts[x][y].set_text(str(pos))
            remove_symbols[x][y].set_text('')
            if i == step - 1:
                # show the image
                img = mpimg.imread(CHESS_PIECE_IMG)
                imagebox = OffsetImage(img, zoom=0.12)
                ab = AnnotationBbox(imagebox, (y + 0.5, x + 0.5),
                                    frameon=False)
                ax.add_artist(ab)
                # adjust the style and position of text to match the image
                texts[x][y].set_color('white')
                texts[x][y].set_zorder(10)
                texts[x][y].set_position((y + 0.47, x + 0.66))
            else:
                # reset the style and position of text
                texts[x][y].set_color('black')
                texts[x][y].set_position((y + 0.5, x + 0.5))
        else:
            chessboard[x, y] = -1  # Reset the cell during backtracking
            # texts[x][y].set_text('')
            remove_symbols[x][y].set_text('x')
            remove_symbols[x][y].set_zorder(10)
    fig.canvas.draw_idle()


# Continue the step
def continue_step(e):
    global step
    if step < len(moves):
        step += 1
    update()


# Reverse the step
def reverse_step(e):
    global step
    if step > 0:
        step -= 1
    update()


# Solve the knight's tour and store moves
kt = KnightsTour(ROWS, COLS, START_ROW, START_COL)
kt.solve()
moves = kt.getMoves()

# Add continue button
axcontinue = plt.axes([0.25, 0.05, 0.15, 0.075])
bcontinue = Button(axcontinue, 'Continue')
bcontinue.on_clicked(continue_step)

# Add reverse button
axreverse = plt.axes([0.45, 0.05, 0.15, 0.075])
breverse = Button(axreverse, 'Reverse')
breverse.on_clicked(reverse_step)

# Add option to quit
axquit = plt.axes([0.65, 0.05, 0.15, 0.075])
bquit = Button(axquit, 'Quit')
bquit.on_clicked(lambda e: plt.close())

# Display the animation
plt.show()
