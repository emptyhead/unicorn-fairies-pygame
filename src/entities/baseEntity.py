import pygame

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, color="white", size=(50, 50)):
        super().__init__() # Initializes the pygame Sprite logic
        
        # Placeholder setup
        self.image = pygame.Surface(size)
        self.image.fill(color)
        
        # Every entity needs a position (rect)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Movement variables
        self.direction = pygame.Vector2()
        self.speed = 5

    def update(self):
        """Logic that runs every frame."""
        pass