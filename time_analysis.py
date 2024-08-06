import time
import matplotlib.pyplot as plt
from knightstour import KnightsTour


def time_analysis(board_sizes):
    times = []

    for size in board_sizes:
        rows, cols = size
        kt = KnightsTour(rows, cols, 0, 0)

        start_time = time.time()
        kt.solve()
        end_time = time.time()

        elapsed_time = end_time - start_time
        times.append(elapsed_time)

        print(f"Board size {rows}x{cols}: {elapsed_time:.4f} seconds")

    return times


def plot_results(board_sizes, times):
    sizes = [f"{rows}x{cols}" for rows, cols in board_sizes]

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, marker='o')
    plt.xlabel('Board Size')
    plt.ylabel('Time (seconds)')
    plt.title('Knight\'s Tour Time Analysis')
    plt.grid(True)
    # save the plot
    plt.savefig('time_analysis.png')
    plt.show()


def save_results(board_sizes, times):
    with open('time_analysis.txt', 'w') as f:
        f.write('rows,cols,time\n')
        for size, t in zip(board_sizes, times):
            t = round(t, 5)
            f.write(f"{size[0]},{size[1]},{t}\n")


if __name__ == "__main__":
    # Define the board sizes to test
    # why does 5x6 take so long?
    board_sizes = [(3, 4), (4, 4), (4, 5), (5, 5), (6, 5), (6, 6), (6, 7), (7, 7), (8, 8)]

    # Perform the time analysis
    times = time_analysis(board_sizes)

    # Plot the results and save the data
    plot_results(board_sizes, times)
    save_results(board_sizes, times)
