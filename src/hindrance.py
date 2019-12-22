import pygame


class Hindrance():
    """A hindrance object that consists out of an upper and a bottom part with a gap in between.

    :param int x: The x coordinate of the object.
    :param int height: The height of the object.
    :param int gap_y: The upper starting point of the gap.
    :param int width: The width in x pixels the object has.
    :param int gap_size: The size of the gap between the two parts.
    """

    def __init__(self, x, height, gap_y, width=60, gap_size=180):
        self.gap_y = gap_y
        self.x = x
        self.height = height
        self.top = pygame.Rect(self.x, 0, width, self.gap_y)
        self.bottom = pygame.Rect(
            self.x, self.gap_y + gap_size, width, self.height)
        self.was_passed = bool(0)

    def draw(self, screen):
        """Draw a hindrance on the screen.

        :param Screen screen: A screen instance to draw on.
        """

        pygame.draw.rect(screen, pygame.Color(0, 150, 0), self.top)
        pygame.draw.rect(screen, pygame.Color(0, 150, 0), self.bottom)

    def move_x(self, x):
        """Move a hindrance in x direction.

        :param int x: The amount of pixels to move.
        """

        self.x += x
        self.top = self.top.move(x, 0)
        self.bottom = self.bottom.move(x, 0)
