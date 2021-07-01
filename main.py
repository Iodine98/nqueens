import numpy as np
import random

random.seed(2)


class Chessboard:
    def __init__(self, no_of_queens):
        self.no_of_queens = no_of_queens
        self.grid = np.zeros((no_of_queens, no_of_queens))


class OldChessboard(Chessboard):

    def get_left_offset(self, placement):
        return self.no_of_queens - 1 - placement[1]

    def get_right_offset(self, placement):
        return placement[1] - placement[0]

    def get_left_diagonal(self, placement):
        left_offset = self.get_left_offset(placement)
        return np.diagonal(np.fliplr(self.grid), offset=left_offset)

    def get_right_diagonal(self, placement):
        right_offset = self.get_right_offset(placement)
        return np.diagonal(self.grid, offset=right_offset)

    def diagonal_is_valid(self, placement):
        right_diagonal_valid = not np.any(self.get_right_diagonal(placement))
        left_diagonal_valid = not np.any(self.get_left_diagonal(placement))
        return right_diagonal_valid and left_diagonal_valid

    def row_is_valid(self, placement):
        return not np.any(self.grid[placement[0]])

    def column_is_valid(self, placement):
        return not np.any(self.grid.T[placement[1]])

    def is_valid_placement(self, placement) -> bool:
        return self.row_is_valid(placement) and self.column_is_valid(placement) and self.diagonal_is_valid(placement)

    def place_queen(self, placement):
        if self.is_valid_placement(placement):
            self.grid[placement] = 1
            print("Queen placed at ", placement)
        else:
            print("Invalid placement for Queen")

    def place_queen_optimized(self, placement):
        if self.is_valid_placement(placement):
            self.grid[placement[0]] = -1
            self.grid[:, placement[1]] = -1
            indices_left_diagonal = np.where(np.fliplr(np.eye(self.no_of_queens, k=self.get_left_offset(placement))) == 1)
            indices_right_diagonal = np.where(np.eye(self.no_of_queens, k=self.get_right_offset(placement)) == 1)
            self.grid[indices_left_diagonal] = -1
            self.grid[indices_right_diagonal] = -1
            self.grid[placement] = 1
            print("Queen placed at ", placement)
        else:
            print("Invalid placement for Queen")

    def remove_queen(self, placement):
        self.grid[placement[0]] = 0
        self.grid[:, placement[1]] = 0
        indices_left_diagonal = np.where(np.fliplr(np.eye(self.no_of_queens, k=self.get_left_offset(placement))) == 1)
        indices_right_diagonal = np.where(np.eye(self.no_of_queens, k=self.get_right_offset(placement)) == 1)
        self.grid[indices_left_diagonal] = 0
        self.grid[indices_right_diagonal] = 0
        self.grid[placement] = 0
        self.grid[placement] = 0
        print("Queen removed from ", placement)


class NewChessboard(Chessboard):
    pass


if __name__ == '__main__':
    satisfied = False
    queens = 4
    chessboard = OldChessboard(queens)
    chessboard.place_queen_optimized((0, 1))
    while np.array(np.where(chessboard.grid == 0)).shape[1] > 0:




    print(chessboard.grid)
