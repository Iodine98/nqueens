from typing import Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from chessboard import find_solution_nqueens_puzzle


def run_loop(max_number, run_fn):
    x_axis = list(range(4, max_number, 4))
    time_elapsed = []
    for initial_queens in tqdm(x_axis):
        time_elapsed.append(run_fn(initial_queens))
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


run_old(4, write_to_file='nqueens_thirty.csv')
