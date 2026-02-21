import pygame
from .settings import *
from .states import MenuState

class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        self.clock = pygame.time.Clock()
        self.running = True
        self.delta_time = 0  # Time since last frame in seconds

        # Global display settings
        self.invert_need_bars = True   # When True, need bars deplete instead of fill
        self.show_need_bars = True      # When True, need bars are drawn above unicorns
        self.show_name = True           # When True, unicorn name is drawn above the sprite
        self.show_description = True    # When True, unicorn description is drawn above the sprite

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

            # Calculate delta time before update
            self.delta_time = self.clock.tick(FPS) / 1000.0  # Convert ms to seconds

            # 2 delegate to current state
            self.state.handle_events(events)
            self.state.update(self.delta_time)

            # 3 draw the current state
            self.screen.fill("black") # Clear screen before drawing
            self.state.draw(self.screen)
            pygame.display.flip()
        pygame.quit()