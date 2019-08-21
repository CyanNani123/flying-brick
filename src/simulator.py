from screen import *
import threading

def game_execution():
    '''standard main function for player interaction'''
    while True:
        f.run()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN: 
                if e.key == 32:
                    f.brick_jump()
            elif e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit()
        
if __name__ == "__main__": 
    '''run game in a separate thread and trigger events automatically with this algorithm'''
    s = Screen()
    f = Flyingbrick(s.screen)
    try:
        t = threading.Thread(target=game_execution)
        t.start()
        while True:    
            pygame.event.pump()
            time.sleep(0.03)
            #keep brick height at level big enough to pass hindrance
            if len(f.object_buffer):
                if f.object_buffer[0].bottom.y-58 < f.brick.y:             
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key':pygame.K_SPACE}))
            #start game when there is no hindrance
            else:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key':pygame.K_SPACE}))
    except pygame.error:
        raise SystemExit()