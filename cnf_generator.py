from tqdm import tqdm
import itertools
import numpy as np


def generate_dimacs_cnf(queens: int, k_choice=2):
    rows = np.arange(1, queens ** 2 + 1).reshape((queens, queens))
    clauses = [*rows.tolist()]
    for i in tqdm(range(queens), desc="rows"):
        clauses = [*clauses, *map(list, itertools.combinations(-rows[i], k_choice))]
    columns = rows.T
    clauses = [*clauses, *columns.tolist()]
    for j in tqdm(range(queens), desc="columns"):
        clauses = [*clauses, *map(list, (itertools.combinations(-columns[j], k_choice)))]
    offset_range = range(-queens + 2, queens - 1)
    for i in tqdm(offset_range, desc="diagonals"):
        diagonal = -np.diag(rows, i)
        clauses = [*clauses, *map(list, (itertools.combinations(diagonal, k_choice)))]
        flipped_diagonal = -np.diag(np.fliplr(rows), i)
        clauses = [*clauses, *map(list, (itertools.combinations(flipped_diagonal, k_choice)))]
    return clauses


def write_clauses_to_file(queens, clauses, filepath):
    with open(filepath, 'w') as file:
        file.write(f"p cnf {queens ** 2} {len(clauses)}\n")
        for clause in clauses:
            clause_str = ""
            for literal in clause:
                clause_str += str(literal) + " "
            clause_str += "0\n"
            file.write(clause_str)


def show_grid(satisfactory_configuration, queens):
    arr = np.array(satisfactory_configuration).reshape((queens, queens))
    arr = arr > 0
    print(arr)


def read_from_results(queens, filepath='results.txt'):
    configuration = []
    with open(filepath, 'r') as file:
        while True:
            line = file.readline()
            if len(line) == 0:
                break
            if line[0] == 'v':
                text_line = line.split(" ")
                text_line.pop(0)
                text_line.pop()
                configuration = [*configuration, *list(map(int, text_line))]
    arr = np.array(configuration).reshape((queens, queens))
    arr = np.where(arr > 0, 1, 0)
    print(arr)
    return arr


def every_row_has_only_one_queen(arr):
    for row in range(arr.shape[0]):
        count = np.count_nonzero(arr[row] > 0)
        if count == 0 or count > 1:
            return False
    return True



