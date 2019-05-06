from flyingbrick import *
from screen import *

if __name__ == "__main__": 
    '''main method, init screen and run game'''
    s = Screen()
    f = Flyingbrick(s.screen)
    try:
        while True:
            f.run()
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN: 
                    if e.key == 32:
                        f.brick_jump()
                elif e.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit()
    except pygame.error:
        raise SystemExit()