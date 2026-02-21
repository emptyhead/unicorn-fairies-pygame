import pygame

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, color="white", size=(50, 50)):
        super().__init__() # Initializes the pygame Sprite logic
        
        # Placeholder setup
        self.image: pygame.Surface = pygame.Surface(size)
        self.image.fill(color)
        
        # Every entity needs a position (rect)
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))
        
        # Movement variables
        self.direction = pygame.Vector2()
        self.speed = 5

    def update(self):
        """Logic that runs every frame."""
        pass

    def draw(self, surface):
        """Draw the entity to the given surface.
        
        Args:
            surface: The pygame surface to draw the entity on (typically the screen).
        """
        surface.blit(self.image, self.rect)