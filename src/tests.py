import sys
import os
import unittest
import threading
from flyingbrick import *
from screen import *


class TestScreen(unittest.TestCase):
    """Tests the screen object."""

    def test_screen_size_on_init(self):
        """Check the screen size."""

        s = Screen()
        self.assertEqual((400, 600), s.screen.get_size())


class TestFlyingBrick(unittest.TestCase):
    """Tests the game instance."""

    def test_brickjump(self):
        """Check if the brick can jump."""

        s = Screen()
        f = Flyingbrick(s.screen)
        self.assertEqual(f.init, 0)
        self.assertEqual(f.brick_velocity, f.gravity)
        f.brick_jump()
        self.assertEqual(f.init, 1)
        self.assertEqual(f.brick_velocity, f.jump_velocity)

    def test_apply_gravity(self):
        """Check if the gravity is applied correctly."""

        s = Screen()
        f = Flyingbrick(s.screen)
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)
        f.apply_gravity()
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40 + f.brick_velocity)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)

    def test_boundary_check_negative(self):
        """Negative test if boundary check is working correctly."""

        s = Screen()
        f = Flyingbrick(s.screen)
        f.brick = f.brick.move(0, 1)
        f.score = 0
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40 + 1)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        f.boundary_check()
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40 + 1)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)

    def test_boundary_check_top(self):
        """Check if boundary check is working correctly at a top collision."""

        s = Screen()
        f = Flyingbrick(s.screen)
        f.brick = f.brick.move(0, -1000)
        f.score = 0
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40 - 1000)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        f.boundary_check()
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)

    def test_boundary_check_bottom(self):
        """Check if boundary check is working correctly at a bottom collision."""

        s = Screen()
        f = Flyingbrick(s.screen)
        f.brick = f.brick.move(0, 1000)
        f.score = 0
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40 + 1000)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        f.boundary_check()
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)

    def test_boundary_check_hindrance_passes(self):
        """Check if boundary check is working correctly when a hindrance is passed."""

        s = Screen()
        f = Flyingbrick(s.screen)
        # positive test
        f.object_buffer.append(
            Hindrance(-100, f.height, random.randint(100, f.height - 200)))
        self.assertEqual(len(f.object_buffer), 1)
        f.boundary_check()
        self.assertEqual(len(f.object_buffer), 0)
        # negative test
        f.object_buffer.append(
            Hindrance(
                f.width + 40,
                f.height,
                random.randint(
                    100,
                    f.height - 200)))
        self.assertEqual(len(f.object_buffer), 1)
        f.boundary_check()
        self.assertEqual(len(f.object_buffer), 1)

    def test_check_collision_with_hindrance_top(self):
        """Check if boundary check is working correctly when a hindrance is hit at the top."""

        s = Screen()
        f = Flyingbrick(s.screen)
        f.score = 0
        f.object_buffer.append(Hindrance(0, f.height, 500))
        self.assertEqual(len(f.object_buffer), 1)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        f.check_collision_with_hindrance()
        self.assertEqual(len(f.object_buffer), 0)

    def test_check_collision_with_hindrance_bottom(self):
        """Check if boundary check is working correctly when a hindrance is hit at the bottom."""

        s = Screen()
        f = Flyingbrick(s.screen)
        f.score = 0
        f.object_buffer.append(Hindrance(0, f.height, 0))
        self.assertEqual(len(f.object_buffer), 1)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        f.check_collision_with_hindrance()
        self.assertEqual(len(f.object_buffer), 0)

    def test_if_game_initialized(self):
        """Check if the game is initialized correctly."""

        s = Screen()
        f = Flyingbrick(s.screen)
        # negative test
        f.if_game_initialized()
        self.assertEqual(f.score, "Press Space")
        self.assertEqual(len(f.object_buffer), 0)
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)
        # positive test
        f.brick_jump()
        f.if_game_initialized()
        self.assertEqual(f.score, 0)
        self.assertEqual(len(f.object_buffer), 1)
        self.assertEqual(f.brick.x, 10)
        self.assertEqual(f.brick.y, int(f.height / 2) - 40 + f.brick_velocity)
        self.assertEqual(f.brick.height, 40)
        self.assertEqual(f.brick.width, 60)
        
    def test_add_hindrance_to_object_buffer(self):
        """Check if a hindrance is added correctly to the object buffer."""
        
        s = Screen()
        f = Flyingbrick(s.screen)
        self.assertEqual(len(f.object_buffer), 0)
        f.add_hindrance_to_object_buffer()
        self.assertEqual(len(f.object_buffer), 1)

if __name__ == "__main__":
    unittest.main()
