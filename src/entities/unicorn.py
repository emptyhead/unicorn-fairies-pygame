from .baseEntity import BaseEntity
from .sprite_factory import create_unicorn_sprite
import pygame


class Unicorn(BaseEntity):
    # Need decay rates per second (needs increase over time)
    NEED_DECAY_RATES = {
        'love': 2,    # Love need increases by 2 per second
        'play': 3,    # Play need increases by 3 per second
        'food': 4,    # Food need increases by 4 per second
        'sleep': 1.5  # Sleep need increases by 1.5 per second
    }
    
    MAX_NEED_VALUE = 100
    
    # Bar display settings
    BAR_HEIGHT = 8
    BAR_SPACING = 2
    BAR_OFFSET_Y = -25  # Position bars above the sprite
    
    # Colors for each need bar (stat letter, bar color)
    NEED_BAR_COLORS = {
        'love': ((255, 105, 180), 'P'),    # Pink for love (P for Puppies/Love)
        'play': ((255, 165, 0), 'Y'),      # Orange for play (Y for Y/play)
        'food': ((50, 205, 50), 'F'),      # Green for food (F for Food)
        'sleep': ((100, 149, 237), 'S')    # Blue for sleep (S for Sleep)
    }
    
    def __init__(self, name: str, description: str, cost: int, x: int = 0, y: int = 0, size: tuple = (60, 60), color: tuple = (240, 240, 255), mane_color: tuple = (255, 105, 180), horn_color: tuple = (255, 215, 0), use_procedural: bool = True):
        """
        Initialize a Unicorn entity.
        
        Args:
            name: The unicorn's name
            description: Description of the unicorn
            cost: Cost to acquire the unicorn
            x: X position on screen
            y: Y position on screen
            size: Tuple (width, height) for the sprite size
            color: RGB tuple for the unicorn's body color
            mane_color: RGB tuple for the mane and tail color
            horn_color: RGB tuple for the horn color
            use_procedural: If True, use procedural sprite; if False, try to load from assets
        """
        # Store data attributes
        self.name = name
        self.description = description
        self.cost = cost
        self.color = color
        self.mane_color = mane_color
        self.horn_color = horn_color
        self.use_procedural = use_procedural
        self.happiness = 100
        
        # Need variables - start at 0 (no need), increase over time up to MAX_NEED_VALUE
        # Higher value = more urgent need
        self.love_need = 0    # Needs love/affection
        self.play_need = 0    # Needs playtime
        self.food_need = 0    # Needs food
        self.sleep_need = 0   # Needs sleep/rest
        
        # Initialize the sprite/rect from BaseEntity
        super().__init__(x, y, color="white", size=size)
        
        # Replace the default white square with our unicorn sprite
        self.image = create_unicorn_sprite(
            name=name,
            size=size,
            color=color,
            mane_color=mane_color,
            horn_color=horn_color,
            use_procedural=use_procedural
        )
        
        # Update rect to match new image
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, surface):
        """Draw the unicorn and its need bars to the given surface.
        
        Args:
            surface: The pygame surface to draw to (typically the screen).
        """
        # Draw the unicorn sprite
        surface.blit(self.image, self.rect)
        
        # Draw need bars above the sprite
        self.draw_need_bars(surface)
    
    def update(self, delta_time: float = 0):
        """
        Update unicorn needs over time.
        
        Args:
            delta_time: Time elapsed since last frame in seconds (for frame-rate independent updates)
        """
        # Increase needs over time based on decay rates
        # Using per-update with delta_time ensures consistent behavior regardless of frame rate
        self.love_need = min(self.MAX_NEED_VALUE, self.love_need + self.NEED_DECAY_RATES['love'] * delta_time)
        self.play_need = min(self.MAX_NEED_VALUE, self.play_need + self.NEED_DECAY_RATES['play'] * delta_time)
        self.food_need = min(self.MAX_NEED_VALUE, self.food_need + self.NEED_DECAY_RATES['food'] * delta_time)
        self.sleep_need = min(self.MAX_NEED_VALUE, self.sleep_need + self.NEED_DECAY_RATES['sleep'] * delta_time)
        
        # Update happiness based on needs (high needs = lower happiness)
        total_need = self.love_need + self.play_need + self.food_need + self.sleep_need
        self.happiness = max(0, 100 - (total_need / 4))
    
    def feed(self, food: str):
        """Feed the unicorn and adjust happiness."""
        self.food_need = max(0, self.food_need - 15)
        print(f"{self.name} had food! Food need: {self.food_need}")
    
    def give_love(self):
        """Give the unicorn love/affection to reduce love need."""
        self.love_need = max(0, self.love_need - 25)
        print(f"{self.name} received love! Love need: {self.love_need}")
    
    def play(self):
        """Play with the unicorn to reduce play need."""
        self.play_need = max(0, self.play_need - 30)
        print(f"{self.name} had fun playing! Play need: {self.play_need}")
    
    def sleep(self):
        """Let the unicorn sleep to reduce sleep need."""
        self.sleep_need = max(0, self.sleep_need - 40)
        print(f"{self.name} had a rest! Sleep need: {self.sleep_need}")
    
    def get_status(self) -> dict:
        """Get current status of all needs."""
        return {
            'name': self.name,
            'happiness': self.happiness,
            'love_need': self.love_need,
            'play_need': self.play_need,
            'food_need': self.food_need,
            'sleep_need': self.sleep_need
        }
    
    def draw_need_bars(self, surface: pygame.Surface):
        """
        Draw need bars above the unicorn sprite.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Font for the stat letter
        font = pygame.font.Font(None, 12)
        
        # Get the sprite width
        sprite_width = self.rect.width
        
        # Starting Y position for bars (above the sprite)
        start_y = self.rect.top + self.BAR_OFFSET_Y
        
        # Order: love, play, food, sleep
        needs = [
            ('love', self.love_need),
            ('play', self.play_need),
            ('food', self.food_need),
            ('sleep', self.sleep_need)
        ]
        
        current_y = start_y
        
        for need_name, need_value in needs:
            color, letter = self.NEED_BAR_COLORS[need_name]
            
            # Draw the letter to the left of the bar
            letter_surface = font.render(letter, True, color)
            letter_rect = letter_surface.get_rect()
            letter_rect.left = self.rect.left - 12
            letter_rect.centery = current_y + self.BAR_HEIGHT // 2
            surface.blit(letter_surface, letter_rect)
            
            # Background bar (black)
            bg_rect = pygame.Rect(self.rect.left, current_y, sprite_width, self.BAR_HEIGHT)
            pygame.draw.rect(surface, (0, 0, 0), bg_rect)
            
            # Foreground bar (colored, fills based on need value)
            fill_width = int(sprite_width * (need_value / self.MAX_NEED_VALUE))
            if fill_width > 0:
                fill_rect = pygame.Rect(self.rect.left, current_y, fill_width, self.BAR_HEIGHT)
                pygame.draw.rect(surface, color, fill_rect)
            
            # Border (white outline)
            pygame.draw.rect(surface, (255, 255, 255), bg_rect, 1)
            
            # Move to next bar position
            current_y += self.BAR_HEIGHT + self.BAR_SPACING
