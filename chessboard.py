from abc import ABC, abstractmethod
from typing import Tuple, List
from tqdm import tqdm
from numpy import ndarray
import numpy as np
import random
from numpy.random import default_rng
import sys


class Chessboard(ABC):
    def __init__(self, no_of_queens):
        self.no_of_queens = no_of_queens
        self.grid = np.zeros((no_of_queens, no_of_queens), dtype=int)

    @abstractmethod
    def get_left_offset(self, placement) -> int:
        return self.no_of_queens - 1 - placement[1] - placement[0]

    @abstractmethod
    def get_right_offset(self, placement) -> int:
        return placement[1] - placement[0]

    def get_left_diagonal(self, placement) -> ndarray:
        left_offset = self.get_left_offset(placement)
        return np.diagonal(np.fliplr(self.grid), offset=left_offset)

    def get_right_diagonal(self, placement) -> ndarray:
        right_offset = self.get_right_offset(placement)
        return np.diagonal(self.grid, offset=right_offset)

    @abstractmethod
    def place_queen(self, placement) -> int:
        pass

    @abstractmethod
    def remove_queen(self, placement) -> int:
        pass


class OldChessboard(Chessboard):

    def get_left_offset(self, placement):
        return self.no_of_queens - 1 - placement[1] - placement[0]

    def get_right_offset(self, placement):
        return placement[1] - placement[0]

    def get_left_diagonal(self, placement):
        left_offset = self.get_left_offset(placement)
        return np.diagonal(np.fliplr(self.grid), offset=left_offset)

    def get_right_diagonal(self, placement):
        right_offset = self.get_right_offset(placement)
        return np.diagonal(self.grid, offset=right_offset)

    def diagonal_collisions(self, placement) -> int:
        right_diagonal_collisions = np.count_nonzero(self.get_right_diagonal(placement) == 1)
        left_diagonal_collisions = np.count_nonzero(self.get_left_diagonal(placement) == 1)
        return left_diagonal_collisions + right_diagonal_collisions

    def diagonal_is_valid(self, placement) -> bool:
        right_diagonal_valid = not np.any(np.isin([1], self.get_right_diagonal(placement)))
        left_diagonal_valid = not np.any(np.isin([1], self.get_left_diagonal(placement)))
        return right_diagonal_valid and left_diagonal_valid

    def row_is_valid(self, placement):
        return not np.any(np.isin([1], self.grid[placement[0]]))

    def row_collisions(self, placement):
        return np.count_nonzero(self.grid[placement[0]] == 1)

    def column_is_valid(self, placement):
        return not np.any(np.isin([1], self.grid.T[placement[1]]))

    def column_collisions(self, placement):
        return np.count_nonzero(self.grid.T[placement[1]] == 1)

    def is_valid_placement(self, placement) -> bool:
        return self.row_is_valid(placement) and self.column_is_valid(placement) and self.diagonal_is_valid(placement)

    def calculate_collisions(self, placement) -> int:
        return self.row_collisions(placement) + self.column_collisions(placement) + self.diagonal_collisions(placement)

    def random_placement(self):
        pl = (np.random.choice(self.grid.shape[0]), np.random.choice(self.grid.shape[1]))
        self.place_queen(pl)
        return pl

    def place_queen(self, placement):
        self.grid[placement[0]] = -1
        self.grid[:, placement[1]] = -1
        indices_left_diagonal = np.where(
            np.fliplr(np.eye(self.no_of_queens, k=self.get_left_offset(placement))) == 1)
        indices_right_diagonal = np.where(np.eye(self.no_of_queens, k=self.get_right_offset(placement)) == 1)
        self.grid[indices_left_diagonal] = -1
        self.grid[indices_right_diagonal] = -1
        self.grid[placement] = 1
        return 1

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


def find_solution_nqueens_puzzle_collision_method(initial_queens):
    satisfied = False
    chess_board, queens, free_spots, placements = initialize(initial_queens)
    random_pl = chess_board.random_placement()
    free_spots.remove(list(random_pl))
    loader = tqdm(total=queens ** 4, desc='Options tried')
    while not satisfied:
        if len(free_spots) == 0:
            chess_board, queens, free_spots, placements = initialize(initial_queens)
            chess_board.random_placement()
            free_spots.remove(list(random_pl))
        least_collisions = sys.maxsize
        according_spot = None
        while len(free_spots) > 0:
            free_spot = tuple(random.choice(free_spots))
            coll = chess_board.calculate_collisions(free_spot)
            if coll < least_collisions:
                least_collisions = coll
                according_spot = free_spot
                if least_collisions == 0:
                    free_spots.remove(list(free_spot))
                    break
            free_spots.remove(list(free_spot))
        if queens > 0 and according_spot is not None:
            queens -= chess_board.place_queen(according_spot)
            placements.append(according_spot)
            free_spots = np.array(np.where(chess_board.grid == 0)).T.tolist()
            loader.update(1)
        if queens == 0:
            satisfied = True
    return chess_board, placements


def find_solution_nqueens_puzzle(initial_queens) -> Tuple[Chessboard, List[Tuple[int, int]]]:
    satisfied = False
    chess_board, queens, free_spots, placements = initialize(initial_queens)
    while not satisfied:
        chess_board, queens, free_spots, placements = initialize(initial_queens)
        while len(free_spots) > 0 and queens > 0:
            free_spot = tuple(random.choice(free_spots))
            queens -= chess_board.place_queen(free_spot)
            placements.append(free_spot)
            free_spots = np.array(np.where(chess_board.grid == 0)).T.tolist()
            if queens == 0:
                satisfied = True
    return chess_board, placements


def initialize(no_of_queens, chessboard_size=0, initial_placement=None, grid=None):
    chessboard = OldChessboard(no_of_queens)
    if chessboard_size > no_of_queens:
        chessboard = OldChessboard(chessboard_size)
    if grid is not None:
        chessboard.grid = grid
    if initial_placement is not None:
        chessboard.place_queen(initial_placement)
        return chessboard, no_of_queens - 1, np.array(np.where(chessboard.grid == 0)).T.tolist(), [initial_placement]
    return chessboard, no_of_queens, np.array(np.where(chessboard.grid == 0)).T.tolist(), []
