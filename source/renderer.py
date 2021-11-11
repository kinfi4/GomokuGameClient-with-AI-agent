import pygame as pg

import const


class Renderer:
    def __init__(self, screen: pg.Surface, board_padding=35):
        self.screen = screen
        self.padding = board_padding
        self.line_size = (self.screen.get_size()[0] - self.padding*2) // (const.BOARD_SIZE - 1)  # with current configuration its 46

    def draw_board_lines(self):
        for i in range(const.BOARD_SIZE):

            # Drawing vertical lines
            if i == const.BOARD_SIZE - 1:
                start_pos = (self.screen.get_size()[0] - self.padding, self.padding)
                end_pos = (self.screen.get_size()[0] - self.padding, self.screen.get_size()[0] - self.padding)
            else:
                start_pos = (self.padding + i*self.line_size, self.padding)
                end_pos = (self.padding + i*self.line_size, self.screen.get_size()[0] - self.padding)

            pg.draw.line(self.screen, const.Color.LIGHTER_BLACK, start_pos, end_pos, width=2)

            # Drawing horizontal lines
            if i == const.BOARD_SIZE - 1:
                start_pos = (self.padding, self.screen.get_size()[0] - self.padding)
                end_pos = (self.screen.get_size()[0] - self.padding, self.screen.get_size()[0] - self.padding)
            else:
                start_pos = (self.padding, self.padding + i*self.line_size)
                end_pos = (self.screen.get_size()[0] - self.padding, self.padding + i*self.line_size)

            pg.draw.line(self.screen, const.Color.LIGHTER_BLACK, start_pos, end_pos, width=2)

        pg.display.update()

    def place_checker(self, pos_x, pos_y, checker_type):
        checker_color = const.Color.BLACK if checker_type == const.CheckerType.BLACK else const.Color.WHITE
        checker_second_color = const.Color.LIGHTER_BLACK if checker_type == const.CheckerType.BLACK else const.Color.A_BIT_YELLOW_WHITE

        pg.draw.circle(self.screen, checker_color, center=(pos_x, pos_y), radius=26)
        pg.draw.circle(self.screen, checker_second_color, center=(pos_x + 10, pos_y + 4), radius=8)

