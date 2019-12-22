from flyingbrick import *
from screen import *
import sys
import threading


def game_execution(f):
    """Standard main function for player interaction.
    Executes the game interface.

    :param Flyingbrick f: A game instance of flyingbrick.
    """

    while True:
        f.run()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == 32:
                    f.brick_jump()
            elif e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit()


def game_simulation(f):
    """A simulation of the game that runs endless.
    Executes the game interface in a thread and sends input via an algorithm.

    :param Flyingbrick f: A game instance of flyingbrick.
    """

    t = threading.Thread(target=game_execution, args=[f, ])
    t.start()
    while True:
        pygame.event.pump()
        time.sleep(0.03)
        # keep brick height at level big enough to pass hindrance
        if len(f.object_buffer):
            if f.object_buffer[0].bottom.y - 58 < f.brick.y:
                pygame.event.post(
                    pygame.event.Event(
                        pygame.KEYDOWN, {
                            'key': pygame.K_SPACE}))
        # start game when there is no hindrance
        else:
            pygame.event.post(
                pygame.event.Event(
                    pygame.KEYDOWN, {
                        'key': pygame.K_SPACE}))


def cli():
    """The command line interface main entrypoint."""

    if len(sys.argv) == 1:
        sys.argv.append(None)

    s = Screen()
    f = Flyingbrick(s.screen)

    try:
        if sys.argv[1] == "--simulate":
            game_simulation(f)
        elif sys.argv[1] is not None:
            print("python main.py [--help] [--simulate]")
        else:
            game_execution(f)
    except pygame.error:
        raise SystemExit()


if __name__ == "__main__":
    cli()
