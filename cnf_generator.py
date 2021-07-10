import numpy as np
from chessboard import Chessboard, find_solution_nqueens_puzzle

queens: int = 3
clauses = np.zeros((0, queens), dtype=int)
rows = np.arange(1, queens ** 2 + 1).reshape((queens, queens))
print(rows)
clauses = np.vstack((clauses, rows))

not_rows = -rows
clauses = np.vstack((clauses, not_rows))
columns = rows.T
clauses = np.vstack((clauses, columns))
not_columns = -columns
clauses = np.vstack((clauses, not_columns))
diagonals = np.zeros((2 * queens, queens), dtype=int)
offset_range = range(-queens + 2, queens - 1)

for i in offset_range:
    j = i + queens - 2
    diagonal = np.diag(rows, i)
    diagonals[j, :diagonal.shape[0]] = diagonal
    flipped_diagonal = np.diag(np.fliplr(rows), i)
    diagonals[j + queens, :flipped_diagonal.shape[0]] = flipped_diagonal
clauses = np.vstack()

np.savetxt('rows.txt', rows, fmt='%d', delimiter=' ')
