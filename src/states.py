import pygame

class State:
    """Base class for all game states."""
    def __init__(self, game):
        self.game = game

    def handle_events(self, events): pass
    def update(self): pass
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
    def update(self):
        # Game logic goes here
        pass

    def draw(self, screen):
        screen.fill("green") # Placeholder for Level 1