import pygame as pg
import pygame_menu

from game_controller import Gomoku
from const import SCREEN_SIZE

pg.init()


def start_menu():
    menu = pygame_menu.Menu('Postav\'te 6 pg', SCREEN_SIZE[0], SCREEN_SIZE[0], theme=pygame_menu.themes.THEME_DARK)

    menu.add.selector('Difficulty :', [('Hard', 1), ('Medium', 2), ('Low', 3)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)


def set_difficulty(value, *args):
    global difficulty
    difficulty = value[0][0]


def start_the_game():
    game = Gomoku(difficulty=difficulty, screen=screen)
    game.main_loop()


if __name__ == '__main__':
    screen = pg.display.set_mode(SCREEN_SIZE)
    difficulty = None

    start_menu()
