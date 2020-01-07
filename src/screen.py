import pygame
import os


class Screen():
    """The game screen where contents are displayed.

    :param int width: The screens width.
    :param int height: The screens height.
    """

    def __init__(self, width=400, height=600, headless=False):
        if headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(pygame.Color(255, 255, 255))
        pygame.display.init()
        pygame.display.update()
