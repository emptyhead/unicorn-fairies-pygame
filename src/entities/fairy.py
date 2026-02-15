from .baseEntity import BaseEntity
from .sprite_factory import create_fairy_sprite


class Fairy(BaseEntity):
    def __init__(self, name: str, description: str, cost: int, x: int = 0, y: int = 0, size: tuple = (50, 50), color: tuple = (255, 200, 150), wing_color: tuple = (200, 230, 255), use_procedural: bool = True):
        """
        Initialize a Fairy entity.
        
        Args:
            name: The fairy's name
            description: Description of the fairy
            cost: Cost to acquire the fairy
            x: X position on screen
            y: Y position on screen
            size: Tuple (width, height) for the sprite size
            color: RGB tuple for the fairy's body color
            wing_color: RGB tuple for the wing color
            use_procedural: If True, use procedural sprite; if False, try to load from assets
        """
        # Store data attributes
        self.name = name
        self.description = description
        self.cost = cost
        self.color = color
        self.wing_color = wing_color
        self.use_procedural = use_procedural
        
        # Initialize the sprite/rect from BaseEntity
        super().__init__(x, y, color="white", size=size)
        
        # Replace the default white square with our fairy sprite
        self.image = create_fairy_sprite(
            name=name,
            size=size,
            color=color,
            wing_color=wing_color,
            use_procedural=use_procedural
        )
        
        # Update rect to match new image
        self.rect = self.image.get_rect(topleft=(x, y))