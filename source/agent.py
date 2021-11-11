from copy import deepcopy

from const import CheckerType, BOARD_SIZE
from board import Board


class Agent:
    difficulties_to_depth = {
        'low': 3,
        'medium': 4,
        'hard': 5
    }

    def __init__(self, difficulty='low'):
        self.difficulty = difficulty

    def make_move(self, current_board, color_making_move):
        depth = self.difficulties_to_depth[self.difficulty]

        _, new_board = self.minimax(current_board, depth, color_making_move, float('-inf'), float('inf'))
        return new_board

    def minimax(self, board: Board, depth, color_making_move, i_alpha, i_beta):
        if depth == 0 or board.is_game_winner(color_making_move):
            return board.evaluate_board(), board

        best_board = None

        if color_making_move == CheckerType.WHITE:
            for new_board in self.get_all_possible_children_boards(board, color_making_move):
                new_evaluation, _ = self.minimax(new_board, depth - 1, CheckerType.BLACK, i_alpha, i_beta)

                if new_evaluation >= i_alpha:
                    i_alpha = new_evaluation
                    best_board = new_board

                if i_beta <= i_alpha:
                    break

            return i_alpha, best_board

        else:
            for new_board in self.get_all_possible_children_boards(board, color_making_move):
                new_evaluation, _ = self.minimax(new_board, depth - 1, CheckerType.WHITE, i_alpha, i_beta)

                if new_evaluation <= i_beta:
                    i_beta = new_evaluation
                    best_board = new_board

                if i_beta <= i_alpha:
                    break

            return i_beta, best_board

    def get_all_possible_children_boards(self, board, color_making_move):
        boards = []

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if board.board[y][x] == CheckerType.EMPTY and self.checker_has_a_neighbor(board.board, (x, y)):
                    board_copy = deepcopy(board)
                    board_copy.board[y][x] = color_making_move
                    boards.append(board_copy)

        return boards

    @staticmethod
    def checker_has_a_neighbor(board, checker_pos):
        x, y = checker_pos

        if x > 0 and board[y][x - 1] != CheckerType.EMPTY:
            return True

        if x < BOARD_SIZE - 1 and board[y][x + 1] != CheckerType.EMPTY:
            return True

        if y > 0 and board[y - 1][x] != CheckerType.EMPTY:
            return True

        if y < BOARD_SIZE - 1 and board[y + 1][x] != CheckerType.EMPTY:
            return True

        if x > 0 and y > 0 and board[y - 1][x - 1] != CheckerType.EMPTY:
            return True

        if x > 0 and y < BOARD_SIZE -1 and board[y + 1][x - 1] != CheckerType.EMPTY:
            return True

        if x < BOARD_SIZE - 1 and y > 0 and board[y - 1][x + 1] != CheckerType.EMPTY:
            return True

        if x < BOARD_SIZE - 1 and y < BOARD_SIZE - 1 and board[y + 1][x + 1] != CheckerType.EMPTY:
            return True

        return False
