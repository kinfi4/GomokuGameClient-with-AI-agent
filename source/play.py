import sys

from game_controller import Gomoku


if __name__ == '__main__':
    difficulty = sys.argv[1]

    if difficulty not in ['low', 'medium', 'hard']:
        raise ValueError(f'Invalid difficulty specified, you must choose between: [low, medium, hard], you entered: {difficulty}')

    game = Gomoku(difficulty=difficulty)
    game.main_loop()
