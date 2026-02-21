import pygame

from .entities.fairy import Fairy
from .entities.unicorn import Unicorn

class State:
    """Base class for all game states."""
    def __init__(self, game):
        self.game = game

    def handle_events(self, events): pass
    def update(self, delta_time: float = 0): pass
    def draw(self, screen): pass

class MenuState(State):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_state(PlayingState(self.game))

    def draw(self, screen):
        screen.fill("blue") # Placeholder for Menu

class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)
        # Create unicorn once, not every frame
        self.unicorn = Unicorn("Sparkle", "A magical pink unicorn", 50, x=200, y=200)
        # create a fairy and draw on screen
        self.fairy = Fairy("Fairy", "Description", 10, x=100, y=100)
    
    def update(self, delta_time: float = 0):
        # Update unicorn needs
        self.unicorn.update(delta_time)

    def draw(self, screen):
        screen.fill("darkgreen") # Placeholder for Level 1
        self.fairy.draw(screen)
        # draw the unicorn (created once in __init__)
        self.unicorn.draw(screen)