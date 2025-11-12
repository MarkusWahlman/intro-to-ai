import math
from copy import deepcopy
import time

MAX = 'X'
MIN = 'O'
EMPTY = ' '
class Board:
    def __init__(self, cells):
        self.cells = cells

    def print(self):
        for i, cell in enumerate(self.cells, start=1):
            print(cell, end='')
            if i % 3 == 0:
                print()

    def winner(self):
        win_positions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for (a, b, c) in win_positions:
            if self.cells[a] != EMPTY and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def end_state(self):
        return self.winner() is not None or EMPTY not in self.cells

    def value(self):
        w = self.winner()
        if w == MAX:
            return 1
        elif w == MIN:
            return -1
        else:
            return 0

    def children(self, player):
        next_player = MIN if player == MAX else MAX
        for i in range(9):
            if self.cells[i] == EMPTY:
                new_cells = deepcopy(self.cells)
                new_cells[i] = player
                yield Board(new_cells), i, next_player


def max_value(board):
    if board.end_state():
        return board.value(), None
    v = -math.inf
    best_move = None
    for child, move, next_player in board.children(MAX):
        child_value, _ = min_value(child)
        if child_value > v:
            v = child_value
            best_move = move
    return v, best_move


def min_value(board):
    if board.end_state():
        return board.value(), None
    v = math.inf
    best_move = None
    for child, move, next_player in board.children(MIN):
        child_value, _ = max_value(child)
        if child_value < v:
            v = child_value
            best_move = move
    return v, best_move


if __name__ == "__main__":
    board = Board([
        'O', 'X', 'O',
        'X', ' ', ' ',
        'X', 'O', ' '
    ])

    print("Board:")
    board.print()

    start_time = time.time()
    value, move = min_value(board)
    end_time = time.time()
    print(f"Calculation took {end_time - start_time:.6f} seconds")
    
    print(f"\nMinimax value of position: {value}")
    if move is not None:
        print(f"Optimal move for Min: position {move}")