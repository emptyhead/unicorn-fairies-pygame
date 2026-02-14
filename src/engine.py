import pygame
from .settings import *
from .states import MenuState

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = MenuState(self)

    def change_state(self, new_state):
        self.state = new_state

    def run(self):
        while self.running:
            # 1 get events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # 2 delegate to current state
            self.state.handle_events(events)
            self.state.update()

            # 3 draw the current state
            self.state.fill("black") # Clear screen before drawing
            self.state.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(FPS)
        pygame.quit()