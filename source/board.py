from copy import deepcopy

import pygame as pg
import numpy as np

from renderer import Renderer
from const import CheckerType, BOARD_SIZE


class Board:
    def __init__(self, screen: pg.Surface, init_board_matrix=None):
        self.screen = screen
        self.renderer = Renderer(screen=screen)

        if init_board_matrix is None:
            self.board: np.ndarray = np.full((BOARD_SIZE, BOARD_SIZE), fill_value=CheckerType.EMPTY)
        else:
            self.board = init_board_matrix

    def draw_board(self):
        self.renderer.draw_board_lines()

    def place_checker(self, mouse_pos, checker_type):
        x, y = mouse_pos

        x_index, y_index = x // self.renderer.line_size, y // self.renderer.line_size

        if self.board[y_index, x_index] != CheckerType.EMPTY:
            return self.board[y_index, x_index]

        self.board[y_index, x_index] = checker_type
        self.renderer.place_checker(pos_x=self.renderer.padding + x_index*self.renderer.line_size,
                                    pos_y=self.renderer.padding + y_index*self.renderer.line_size,
                                    checker_type=checker_type)

    def is_game_winner(self, checker_type) -> bool:
        # checking horizontally
        if max(list(self._check_each_row_max_sub_sequence(checker_type))) >= 5:
            return True

        # checking vertically
        if max(list(self._check_each_column_max_sub_sequence(checker_type))) >= 5:
            return True

        # right diagonal
        if max(list(self._get_checker_longest_right_diagonal(checker_type))) >= 5:
            return True

        # left diagonal
        if max(list(self._get_checker_longest_left_diagonal(checker_type))) >= 5:
            return True

        return False

    def evaluate_board(self):
        white_points, black_points = 0, 0

        # checking columns
        for column in self.board.transpose():
            str_col = ''.join(column)
            w_p, b_p = self._get_heuristic_points_of_sequence(str_col)
            white_points += w_p
            black_points += b_p

        # checking rows
        for row in self.board:
            str_row = ''.join(row)
            w_p, b_p = self._get_heuristic_points_of_sequence(str_row)
            white_points += w_p
            black_points += b_p

        # checking right diagonal
        for diagonal in [self.board.diagonal(offset=-x) for x in np.arange(-BOARD_SIZE + 1, BOARD_SIZE)]:
            str_diag = ''.join(diagonal)
            w_p, b_p = self._get_heuristic_points_of_sequence(str_diag)
            white_points += w_p
            black_points += b_p

        # checking left diagonal
        for diagonal in [self.board[::-1].diagonal(offset=-x) for x in np.arange(-BOARD_SIZE + 1, BOARD_SIZE)]:
            str_diag = ''.join(diagonal)
            w_p, b_p = self._get_heuristic_points_of_sequence(str_diag)
            white_points += w_p
            black_points += b_p

        return white_points + black_points

    def redraw_board(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.board[y][x] == CheckerType.EMPTY:
                    continue

                self.renderer.place_checker(pos_x=self.renderer.padding + x*self.renderer.line_size,
                                            pos_y=self.renderer.padding + y*self.renderer.line_size,
                                            checker_type=self.board[y][x])

    def _check_each_column_max_sub_sequence(self, checker_type):
        for column in self.board.transpose():
            str_col = ''.join(column)

            if checker_type in str_col:
                longest_sequence = self._find_max_sub_length_in_string(str_col, checker_type)
                yield longest_sequence

        yield 0

    def _check_each_row_max_sub_sequence(self, checker_type):
        for row in self.board:
            str_row = ''.join(row)

            if checker_type in str_row:
                longest_sequence = self._find_max_sub_length_in_string(str_row, checker_type)
                yield longest_sequence

        yield 0

    def _get_checker_longest_right_diagonal(self, checker_type):
        for diagonal in [self.board.diagonal(offset=-x) for x in np.arange(-BOARD_SIZE + 1, BOARD_SIZE)]:
            str_diag = ''.join(diagonal)

            if checker_type in str_diag:
                longest_sequence = self._find_max_sub_length_in_string(str_diag, checker_type)
                yield longest_sequence

        yield 0

    def _get_checker_longest_left_diagonal(self, checker_type):
        for diagonal in [self.board[::-1].diagonal(offset=-x) for x in np.arange(-BOARD_SIZE + 1, BOARD_SIZE)]:
            str_diag = ''.join(diagonal)

            if checker_type in str_diag:
                longest_sequence = self._find_max_sub_length_in_string(str_diag, checker_type)
                yield longest_sequence

        yield 0

    @staticmethod
    def _get_heuristic_points_of_sequence(string):
        white_points, black_points = 0, 0
        w, b, e = CheckerType.WHITE, CheckerType.BLACK, CheckerType.EMPTY
        if ''.join([w, w, w, w, w]) in string:
            white_points = 100000000000
        elif ''.join([e, w, w, w, w, e]):
            white_points = 100000000000 - 1
        elif ''.join([e, w, w, w, e]):
            white_points = 100000
        elif ''.join([e, w, w, w]):
            white_points = 400
        elif ''.join([w, w, w, e]):
            white_points = 400
        elif ''.join([e, w, w, e]):
            white_points = 50
        elif ''.join([w, w, e]):
            white_points = 20
        elif ''.join([e, w, w]):
            white_points = 20

        if ''.join([b, b, b, b, b]) in string:
            black_points = -100000000
        elif ''.join([e, b, b, b, b, e]):
            black_points = -100000000 + 1
        elif ''.join([e, b, b, b, e]):
            black_points = -10000
        elif ''.join([e, b, b, b]):
            black_points = -800
        elif ''.join([b, b, b, e]):
            black_points = -800
        elif ''.join([e, b, b, e]):
            black_points = -100
        elif ''.join([b, b, e]):
            black_points = -50
        elif ''.join([e, b, b]):
            black_points = -50

        return white_points, black_points

    @staticmethod
    def _find_max_sub_length_in_string(string, char):
        longest_sequence, temp_length = 0, 0
        for i in range(len(string)):
            if string[i] == char:
                temp_length += 1
            else:
                longest_sequence = max(longest_sequence, temp_length)
                temp_length = 0

        longest_sequence = max(longest_sequence, temp_length)
        return longest_sequence

    def __deepcopy__(self, memodict={}):
        return Board(screen=self.screen, init_board_matrix=deepcopy(self.board))

