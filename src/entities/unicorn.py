from .baseEntity import BaseEntity
from .sprite_factory import create_unicorn_sprite
import pygame
import random


class Unicorn(BaseEntity):
    # Wander behaviour constants
    WANDER_SPEED = 50                  # Base wander speed in pixels per second
    WANDER_PAUSE_MIN = 1.0             # Minimum pause duration in seconds
    WANDER_PAUSE_MAX = 3.0             # Maximum pause duration in seconds
    WANDER_ARRIVAL_THRESHOLD = 5       # Distance (px) at which target is considered reached
    WANDER_MARGIN = 10                 # Pixel margin from screen edges when picking a target
    WANDER_SLEEP_SPEED_FACTOR = 0.25   # At max sleep need, speed is reduced to this fraction

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

        # Store the original (unflipped) sprite for directional flipping
        self.original_image = self.image.copy()
        self.facing_right = True

        # Individual display flags
        self.show_need_bars = True      # When True, need bars are drawn above the sprite
        self.show_name = True           # When True, the unicorn's name is drawn above the sprite
        self.show_description = True    # When True, the unicorn's description is drawn above the sprite

        # Need bar display flag — when True, bars deplete as needs increase (full = healthy)
        # When False (default), bars fill as needs increase (full = urgent need)
        self.invert_need_bars = True

        # Wander state machine variables
        self.wander_state = 'idle'                          # 'idle' | 'moving' | 'paused'
        self.wander_target = None                           # pygame.Vector2 target position
        self.wander_pause_timer = 0.0                       # Countdown timer while paused
        self.wander_bounds = (800, 600)                     # (width, height) — updated by the game state
        self.wander_pos = pygame.Vector2(float(x), float(y))  # Sub-pixel float position accumulator
    
    def draw(self, surface):
        """Draw the unicorn, and optionally its need bars, name, and description.

        Args:
            surface: The pygame surface to draw to (typically the screen).
        """
        # Draw the unicorn sprite
        surface.blit(self.image, self.rect)

        # Draw need bars above the sprite (if enabled)
        if self.show_need_bars:
            self.draw_need_bars(surface)

        # Draw name and/or description above the sprite (if either is enabled)
        if self.show_name or self.show_description:
            self.draw_info(surface)
    
    def _pick_wander_target(self) -> pygame.Vector2:
        """Pick a random target position within the screen bounds.

        Returns:
            A pygame.Vector2 representing the target position.
        """
        margin = self.WANDER_MARGIN
        w, h = self.wander_bounds
        x = random.randint(margin, int(max(margin, w - self.rect.width - margin)))
        y = random.randint(margin, int(max(margin, h - self.rect.height - margin)))
        return pygame.Vector2(x, y)

    def _get_wander_speed(self) -> float:
        """Return the effective wander speed, reduced by sleep need.

        At sleep_need == 0  → full WANDER_SPEED (50 px/s).
        At sleep_need == MAX_NEED_VALUE → WANDER_SPEED * WANDER_SLEEP_SPEED_FACTOR (12.5 px/s).

        Returns:
            Effective speed in pixels per second.
        """
        sleep_ratio = self.sleep_need / self.MAX_NEED_VALUE  # 0.0 – 1.0
        speed_factor = 1.0 - sleep_ratio * (1.0 - self.WANDER_SLEEP_SPEED_FACTOR)
        return self.WANDER_SPEED * speed_factor

    def wander(self, delta_time: float):
        """Advance the wander state machine by one frame.

        States:
            idle    → pick first target, transition to 'moving'.
            moving  → move toward wander_target; on arrival transition to 'paused'.
            paused  → count down pause timer; on expiry pick new target, transition to 'moving'.

        Args:
            delta_time: Time elapsed since last frame in seconds.
        """
        if self.wander_state == 'idle':
            self.wander_target = self._pick_wander_target()
            self.wander_state = 'moving'

        elif self.wander_state == 'moving':
            if self.wander_target is None:
                self.wander_target = self._pick_wander_target()

            to_target = self.wander_target - self.wander_pos
            distance = to_target.length()

            if distance <= self.WANDER_ARRIVAL_THRESHOLD:
                # Arrived — stay at current position (no snap), start pause
                self.rect.topleft = (int(self.wander_pos.x), int(self.wander_pos.y))
                self.wander_pause_timer = random.uniform(
                    self.WANDER_PAUSE_MIN, self.WANDER_PAUSE_MAX
                )
                self.wander_state = 'paused'
            else:
                # Move toward target using float accumulator to avoid sub-pixel truncation
                step = to_target.normalize() * self._get_wander_speed() * delta_time

                # Flip sprite based on horizontal direction
                moving_right = to_target.x >= 0
                if moving_right != self.facing_right:
                    self.facing_right = moving_right
                    self.image = pygame.transform.flip(
                        self.original_image, not self.facing_right, False
                    )

                self.wander_pos += step

                # Clamp float position to screen bounds
                w, h = self.wander_bounds
                self.wander_pos.x = max(0.0, min(self.wander_pos.x, float(w - self.rect.width)))
                self.wander_pos.y = max(0.0, min(self.wander_pos.y, float(h - self.rect.height)))

                # Sync rect from float position
                self.rect.topleft = (int(self.wander_pos.x), int(self.wander_pos.y))

        elif self.wander_state == 'paused':
            self.wander_pause_timer -= delta_time
            if self.wander_pause_timer <= 0:
                self.wander_target = self._pick_wander_target()
                self.wander_state = 'moving'

    def update(self, delta_time: float = 0):
        """
        Update unicorn needs over time and advance wander behaviour.
        
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

        # Advance wander behaviour
        self.wander(delta_time)
    
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
    
    def draw_info(self, surface: pygame.Surface):
        """Draw the unicorn's name and/or description above the need bars.

        Each element is only rendered when its corresponding flag is True.
        The name is rendered in white (size 18) and the description in
        light-grey (size 14), both centred horizontally over the sprite.

        Args:
            surface: The pygame surface to draw on.
        """
        name_font = pygame.font.Font(None, 18)
        desc_font = pygame.font.Font(None, 14)
        padding = 2

        # Anchor point: top of the need bars (or top of sprite if bars are hidden)
        bars_top = self.rect.top + self.BAR_OFFSET_Y

        # Build the list of surfaces to stack, bottom-most first
        # Each entry is (surface, rendered_surface) — we stack upward
        stack = []
        if self.show_description:
            stack.append(desc_font.render(self.description, True, (200, 200, 200)))
        if self.show_name:
            stack.append(name_font.render(self.name, True, (255, 255, 255)))

        # Draw from bottom to top, starting just above the bars
        current_bottom = bars_top - padding
        for surf in stack:
            rect = surf.get_rect(centerx=self.rect.centerx, bottom=current_bottom)
            surface.blit(surf, rect)
            current_bottom = rect.top - padding

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
            ratio = need_value / self.MAX_NEED_VALUE
            if self.invert_need_bars:
                ratio = 1.0 - ratio  # Full bar = healthy, depletes as need increases
            fill_width = int(sprite_width * ratio)
            if fill_width > 0:
                fill_rect = pygame.Rect(self.rect.left, current_y, fill_width, self.BAR_HEIGHT)
                pygame.draw.rect(surface, color, fill_rect)
            
            # Border (white outline)
            pygame.draw.rect(surface, (255, 255, 255), bg_rect, 1)
            
            # Move to next bar position
            current_y += self.BAR_HEIGHT + self.BAR_SPACING
