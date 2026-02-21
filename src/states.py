import pygame

from .entities.fairy import Fairy
from .entities.unicorn import Unicorn
from .settings import WIDTH, HEIGHT

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
        # Create unicorns as a list
        self.unicorns = [
            Unicorn("Sparkle", "A magical pink unicorn", 50, x=200, y=200),
            Unicorn("Rosella", "A magical yellow unicorn", 50, x=250, y=200),
        ]
        for u in self.unicorns:
            u.wander_bounds = (WIDTH, HEIGHT)
        # create a fairy and draw on screen
        self.fairy = Fairy("Fairy", "Description", 10, x=100, y=100)

    def update(self, delta_time: float = 0):
        for u in self.unicorns:
            u.update(delta_time)

    def draw(self, screen):
        screen.fill("darkgreen") # Placeholder for Level 1
        self.fairy.draw(screen)
        for u in self.unicorns:
            u.draw(screen)