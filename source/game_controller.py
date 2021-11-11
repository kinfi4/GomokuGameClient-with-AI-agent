import pygame as pg

from const import CheckerType, SCREEN_SIZE, Color, FPS
from board import Board
from agent import Agent

pg.init()


class Gomoku:
    def __init__(self, difficulty):
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.board = Board(screen=self.screen)
        self.agent = Agent(difficulty=difficulty)
        self.game_is_over = False

        self.screen.fill(Color.YELLOW)

        self.current_player_move = CheckerType.WHITE

        pg.display.set_caption('Gomoku')

    def main_loop(self):
        self.board.draw_board()

        while not self.game_is_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            self._check_user_input()

            pg.display.update()
            self.clock.tick(FPS)

    def _check_user_input(self):
        if pg.mouse.get_pressed(3)[0]:

            if self.current_player_move == CheckerType.WHITE:
                try:
                    if element := self.board.place_checker(pg.mouse.get_pos(), CheckerType.WHITE):
                        return
                except IndexError:
                    return
            else:
                self._computer_make_move()
                pass

            if self.board.is_game_winner(self.current_player_move):
                self._draw_game_over(self.current_player_move)
                self.game_is_over = True

            self.current_player_move = CheckerType.WHITE if self.current_player_move == CheckerType.BLACK \
                else CheckerType.BLACK

    def _computer_make_move(self):
        new_board = self.agent.make_move(self.board, CheckerType.BLACK)
        self.board = new_board
        self.board.redraw_board()

    def _draw_game_over(self, winner):
        font = pg.font.SysFont('liberationmono', 60)
        game_over_text = font.render('GAME OVER', True, Color.LIGHT_RED, Color.WHITE)

        s_w, s_h = SCREEN_SIZE
        pos_game_over = game_over_text.get_rect(center=(s_w//2, s_h//2))

        winning_string = 'White is a winner' if winner == CheckerType.WHITE else 'Black is a winner'
        winning_text = font.render(winning_string, True, Color.LIGHT_RED, Color.WHITE)
        pos_winner_text = winning_text.get_rect(center=(s_w//2, s_h//2 + 100))

        self.screen.blit(game_over_text, pos_game_over)
        self.screen.blit(winning_text, pos_winner_text)
        pg.display.update()
        input()
