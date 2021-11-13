from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from chessboard import find_solution_nqueens_puzzle, find_solution_nqueens_puzzle_collision_method, OldChessboard


def run_loop(max_number, run_fn):
    x_axis = list(range(5, max_number + 1, 5))
    time_elapsed = []
    for initial_queens in tqdm(x_axis):
        time_elapsed.append(run_fn(initial_queens))
    fig = plt.figure()
    subpl = fig.add_subplot()
    subpl.set_xlabel('number of queens')
    subpl.set_ylabel('time in seconds')
    plt.plot(x_axis, time_elapsed)
    plt.show()


def run_old(initial_queens: int, write_to_file: Optional[str] = None, print_placements=False):
    a = time.process_time()
    chessboard, placements = find_solution_nqueens_puzzle(initial_queens)
    b = time.process_time()
    print("It took:", b - a, "seconds.")
    if print_placements:
        placements.sort()
        print(placements)
    if write_to_file is not None:
        df = pd.DataFrame(chessboard.grid)
        df.to_csv(write_to_file, header=False, index=False)
    return b - a


fig = plt.figure()
subpl = fig.add_subplot()
subpl.set_xlabel('number of queens')
subpl.set_ylabel('c time')
x_axis: List[int] = [i for i in range(10, 201, 10)]
y_axis: List[float] = [*5 * [0.00], 0.01, 0.00, 0.02, 0.08, 0.08, 0.01, 0.04, 0.03, 0.21, 0.10, 0.17, 0.06, 0.33, 0.26,
                   0.35]
subpl.plot(x_axis, y_axis)
plt.show()

run_loop(50, run_old)
