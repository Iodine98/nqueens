from tqdm import tqdm
import itertools
import numpy as np

queens: int = 4
rows = np.arange(1, queens ** 2 + 1).reshape((queens, queens))
clauses = []
# clauses = [*rows.tolist()]
# for i in range(queens):
#     clauses = [*clauses, *list(map(list, (itertools.combinations(-rows[i], queens - 1))))]
columns = rows.T
# clauses = [*clauses, *columns.tolist()]
# for j in range(queens):
#     clauses = [*clauses, *list(map(list, (itertools.combinations(-columns[j], queens - 1))))]
offset_range = range(-queens + 2, queens - 1)
for i in tqdm(offset_range, desc="diagonals"):
    j = i + queens - 2
    diagonal = -np.diag(rows, i)
    clauses = [*clauses, *list(map(list, (itertools.combinations(diagonal, queens - 1))))]
    flipped_diagonal = -np.diag(np.fliplr(rows), i)
    clauses = [*clauses, *list(map(list, (itertools.combinations(flipped_diagonal, queens - 1))))]
print(clauses)

# clause_list = [[*filter(lambda x: x != 0, clause), 0] for clause in tqdm(clause_list)]
# with open("clauses.cnf", 'w') as file:
#     for clause in clause_list:
#         clause_str = ""
#         for literal in clause:
#             clause_str += str(literal) + " "
#         clause_str += "\n"
#         file.write(clause_str)
