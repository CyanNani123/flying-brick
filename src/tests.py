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
    
    def setUp(self):
        self.s = Screen()
        self.f = Flyingbrick(self.s.screen)

    def test_brickjump(self):
        """Check if the brick can jump."""

        self.assertEqual(self.f.init, 0)
        self.assertEqual(self.f.brick_velocity, self.f.gravity)
        self.f.brick_jump()
        self.assertEqual(self.f.init, 1)
        self.assertEqual(self.f.brick_velocity, self.f.jump_velocity)

    def test_apply_gravity(self):
        """Check if the gravity is applied correctly."""

        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)
        self.f.apply_gravity()
        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40 + self.f.brick_velocity)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)

    def test_boundary_check_negative(self):
        """Negative test if boundary check is working correctly."""

        self.f.brick = self.f.brick.move(0, 1)
        self.f.score = 0
        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40 + 1)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        self.f.boundary_check()
        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40 + 1)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)

    def test_boundary_check_top(self):
        """Check if boundary check is working correctly at a top collision."""

        self.f.brick = self.f.brick.move(0, -1000)
        self.f.score = 0
        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40 - 1000)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        self.f.boundary_check()
        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)

    def test_boundary_check_bottom(self):
        """Check if boundary check is working correctly at a bottom collision."""

        self.f.brick = self.f.brick.move(0, 1000)
        self.f.score = 0
        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40 + 1000)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        self.f.boundary_check()
        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)

    def test_boundary_check_hindrance_passes(self):
        """Check if boundary check is working correctly when a hindrance is passed."""

        # positive test
        self.f.object_buffer.append(
            Hindrance(-100, self.f.height, random.randint(100, self.f.height - 200)))
        self.assertEqual(len(self.f.object_buffer), 1)
        self.f.boundary_check()
        self.assertEqual(len(self.f.object_buffer), 0)
        # negative test
        self.f.object_buffer.append(
            Hindrance(
                self.f.width + 40,
                self.f.height,
                random.randint(
                    100,
                    self.f.height - 200)))
        self.assertEqual(len(self.f.object_buffer), 1)
        self.f.boundary_check()
        self.assertEqual(len(self.f.object_buffer), 1)

    def test_check_collision_with_hindrance_top(self):
        """Check if boundary check is working correctly when a hindrance is hit at the top."""

        self.f.score = 0
        self.f.object_buffer.append(Hindrance(0, self.f.height, 500))
        self.assertEqual(len(self.f.object_buffer), 1)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        self.f.check_collision_with_hindrance()
        self.assertEqual(len(self.f.object_buffer), 0)

    def test_check_collision_with_hindrance_bottom(self):
        """Check if boundary check is working correctly when a hindrance is hit at the bottom."""

        self.f.score = 0
        self.f.object_buffer.append(Hindrance(0, self.f.height, 0))
        self.assertEqual(len(self.f.object_buffer), 1)
        pygame.event.post(
            pygame.event.Event(
                pygame.KEYDOWN, {
                    'key': pygame.K_k}))
        self.f.check_collision_with_hindrance()
        self.assertEqual(len(self.f.object_buffer), 0)

    def test_if_game_initialized(self):
        """Check if the game is initialized correctly."""

        # negative test
        self.f.if_game_initialized()
        self.assertEqual(self.f.score, "Press Space")
        self.assertEqual(len(self.f.object_buffer), 0)
        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)
        # positive test
        self.f.brick_jump()
        self.f.if_game_initialized()
        self.assertEqual(self.f.score, 0)
        self.assertEqual(len(self.f.object_buffer), 1)
        self.assertEqual(self.f.brick.x, 10)
        self.assertEqual(self.f.brick.y, int(self.f.height / 2) - 40 + self.f.brick_velocity)
        self.assertEqual(self.f.brick.height, 40)
        self.assertEqual(self.f.brick.width, 60)
        
    def test_add_hindrance_to_object_buffer(self):
        """Check if a hindrance is added correctly to the object buffer."""
        
        self.assertEqual(len(self.f.object_buffer), 0)
        self.f.add_hindrance_to_object_buffer()
        self.assertEqual(len(self.f.object_buffer), 1)
        
    def test_check_if_hindrance_was_passed(self):
        """Test if the check on passing a hindrance works."""
        
        self.f.brick_jump()
        self.f.add_hindrance_to_object_buffer()
        self.f.object_buffer[0].x = 9
        self.f.check_if_hindrance_was_passed()
        self.assertEqual(self.f.score, 1)
        
    def test_negative_check_if_hindrance_was_passed(self):
        """Test if a negative check on passing a hindrance works."""
        
        self.f.brick_jump()
        self.f.add_hindrance_to_object_buffer()
        self.f.object_buffer[0].x = 10
        self.f.check_if_hindrance_was_passed()
        self.assertEqual(self.f.score, 0)
        

if __name__ == "__main__":
    unittest.main()
