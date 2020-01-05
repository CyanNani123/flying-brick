from hindrance import *
import pygame
import random
import time
import os


class Flyingbrick():
    """The flyingbrick game instance.

    :param Screen screen: The screen to display the game on.

    """

    def __init__(self, screen):
        # reference screen to write into
        self.screen = screen
        pygame.display.set_caption('Flying Brick')
        self.width, self.height = self.screen.get_size()
        # background data
        self.brick = pygame.Rect(10, int(self.height / 2) - 40, 60, 40)
        self.init = bool(0)
        self.score = 'Press Space'

        # initialize pygame font module
        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", 40, bold=True)

        # buffer for hindrances
        self.object_buffer = []

        # physical settings
        self.gravity = 3
        self.hindrance_velocity = 2
        self.brick_velocity = self.gravity
        self.jump_velocity = -25

    def brick_jump(self):
        """Initialize game if not yet done, raise brick velocity to let it jump."""

        if not self.init:
            self.init = bool(1)
            self.score = 0
        self.brick_velocity = self.jump_velocity

    def apply_gravity(self):
        """Move brick according to velocity."""

        self.brick = self.brick.move(0, self.brick_velocity)

    def show_scoretable_after_death(self):
        """Read scoretable from file, write new sorted one to file and display on screen."""

        if os.path.isfile('scoretable.txt'):
            with open('scoretable.txt', 'r') as f:
                scoretable = [line.strip() for line in f]
            f.close()
        else:
            scoretable = []
        scoretable.append(self.score)
        scoretable = sorted(scoretable, key=lambda a: int(a), reverse=True)
        scoretable = scoretable[:5]
        with open("scoretable.txt", "w+") as f:
            for value in scoretable:
                f.write(str(value) + '\n')
        f.close()
        self.draw_background()
        y = 150
        self.screen.blit(
            self.font.render(
                "Highscores", 1, (0, 0, 0)), (self.width / 2 - 130, 100))
        for score in scoretable:
            if score == self.score:
                self.screen.blit(
                    self.font.render(
                        str(score), 1, (255, 0, 0)), (self.width / 2 - 130, y))
            else:
                self.screen.blit(
                    self.font.render(
                        str(score), 1, (0, 0, 0)), (self.width / 2 - 130, y))
            y += 50
        self.screen.blit(
            self.font.render(
                "K to return", 1, (0, 0, 0)), (self.width / 2 - 130, 500))
        pygame.display.update()

    def reset_after_death(self):
        """Show scoretable, reset values to default and wait for keypress after death."""

        self.show_scoretable_after_death()
        self.init = bool(0)
        self.score = 'Press Space'
        self.brick = pygame.Rect(10,
                                 int(self.height / 2) - 40,
                                 self.brick.width,
                                 self.brick.height)
        while True:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == 107:
                        return
                elif e.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit()

    def boundary_check(self):
        """Check boundary collision."""

        # death condition: collide with ceiling or bottom line
        if self.brick.y < 0 or self.brick.y + self.brick.height > self.height:
            self.reset_after_death()
            if len(self.object_buffer):
                self.object_buffer.pop()
        # delete hindrance if it passes the boundary
        if len(self.object_buffer):
            if self.object_buffer[0].x + self.object_buffer[0].top.width < 0:
                self.object_buffer.pop()

    def check_collision_with_hindrance(self):
        """Check collision with hindrance."""

        if self.brick.colliderect(
                self.object_buffer[0].top) or self.brick.colliderect(
                self.object_buffer[0].bottom):
            self.reset_after_death()
            self.object_buffer.pop()
            return True

    def draw_background(self):
        """Draw the game background."""

        pygame.draw.rect(
            self.screen, pygame.Color(
                255, 255, 240), pygame.Rect(
                0, 0, self.width, self.height))

    def draw_score(self):
        """Draw score value or default text."""

        if not isinstance(self.score, str):
            self.screen.blit(self.font.render(
                5 * ' ' + str(self.score), 1, (0, 0, 0)), (self.width / 2 - 130, 50))
        else:
            self.screen.blit(self.font.render(
                str(self.score), 1, (0, 0, 0)), (self.width / 2 - 130, 50))

    def draw_brick_and_score(self):
        """Draw brick and score."""

        pygame.draw.rect(self.screen, pygame.Color(255, 0, 0), self.brick)
        if self.brick_velocity <= self.gravity:
            self.brick_velocity += self.gravity
        else:
            self.brick_velocity = self.gravity
        self.draw_score()
        
    def add_hindrance_to_object_buffer(self):
        """Add hindrance to object buffer."""
        
        self.object_buffer.append(
            Hindrance(
                self.width + 40,
                self.height,
                random.randint(
                    100,
                    self.height - 200)))

    def if_game_initialized(self):
        """If init is true apply gravity, check death conditions and spawn new hindrances."""

        if self.init:
            # create hindrance if there is none
            if not len(self.object_buffer):
                self.add_hindrance_to_object_buffer()
            self.boundary_check()
            # move hindrance, check collision or update
            if len(self.object_buffer):
                if self.check_collision_with_hindrance():
                    return
                if not self.object_buffer[0].was_passed:
                    if self.brick.x > self.object_buffer[0].x:
                        self.object_buffer[0].was_passed = bool(1)
                        self.score += 1
                self.object_buffer[0].move_x(-self.hindrance_velocity)
                self.object_buffer[0].draw(self.screen)
            self.apply_gravity()

    def run(self):
        """Run the game."""

        time.sleep(1 / 100)
        self.draw_background()
        self.if_game_initialized()
        self.draw_brick_and_score()
        pygame.display.update()
