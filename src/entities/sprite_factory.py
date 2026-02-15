"""
Sprite factory module for creating procedural and asset-based sprites.
"""
import pygame
import os


def create_procedural_fairy(size=(50, 50), color=(255, 200, 150), wing_color=(200, 230, 255)):
    """
    Creates a procedural fairy sprite using pygame drawing primitives.
    
    Args:
        size: Tuple (width, height) for the sprite size
        color: RGB tuple for the fairy's body color
        wing_color: RGB tuple for the wing color
    
    Returns:
        pygame.Surface with the fairy sprite drawn on it
    """
    width, height = size
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    center_x = width // 2
    center_y = height // 2
    
    # Draw wings (behind body)
    wing_width = width // 3
    wing_height = height // 2
    
    # Left wing
    pygame.draw.ellipse(
        surface, 
        (*wing_color, 180),  # Add alpha for transparency
        (0, center_y - wing_height // 2, wing_width, wing_height)
    )
    
    # Right wing
    pygame.draw.ellipse(
        surface,
        (*wing_color, 180),
        (width - wing_width, center_y - wing_height // 2, wing_width, wing_height)
    )
    
    # Draw body (circle)
    body_radius = min(width, height) // 4
    pygame.draw.circle(surface, color, (center_x, center_y + body_radius // 2), body_radius)
    
    # Draw head (smaller circle above body)
    head_radius = body_radius // 2
    pygame.draw.circle(surface, color, (center_x, center_y - body_radius // 2), head_radius)
    
    # Draw eyes (small black dots)
    eye_offset = head_radius // 3
    eye_radius = 2
    pygame.draw.circle(surface, (0, 0, 0), (center_x - eye_offset, center_y - body_radius // 2), eye_radius)
    pygame.draw.circle(surface, (0, 0, 0), (center_x + eye_offset, center_y - body_radius // 2), eye_radius)
    
    # Draw glow effect (simple gradient-like circles)
    glow_color = (*wing_color, 50)
    for i in range(3):
        glow_radius = body_radius + (i + 1) * 5
        pygame.draw.circle(
            surface,
            glow_color,
            (center_x, center_y + body_radius // 2),
            glow_radius,
            1
        )
    
    return surface


def create_fairy_from_asset(name: str, size=(50, 50), asset_dir="assets/fairies"):
    """
    Loads a fairy sprite from an asset file.
    
    Args:
        name: The fairy's name (used to find the asset file)
        size: Tuple (width, height) to scale the sprite to
        asset_dir: Directory containing fairy assets
    
    Returns:
        pygame.Surface with the loaded and scaled sprite, or None if not found
    """
    # Convert name to filename (e.g., "Fire Fairy" -> "fire_fairy.png")
    filename = name.lower().replace(" ", "_") + ".png"
    filepath = os.path.join(asset_dir, filename)
    
    if os.path.exists(filepath):
        try:
            sprite = pygame.image.load(filepath).convert_alpha()
            return pygame.transform.scale(sprite, size)
        except pygame.error:
            print(f"Warning: Failed to load fairy asset: {filepath}")
            return None
    
    print(f"Warning: Fairy asset not found: {filepath}")
    return None


def create_fairy_sprite(name: str, size=(50, 50), color=(255, 200, 150), wing_color=(200, 230, 255), use_procedural=True, asset_dir="assets/fairies"):
    """
    Creates a fairy sprite, using procedural generation or assets based on the flag.
    
    Args:
        name: The fairy's name (used to find asset files if not procedural)
        size: Tuple (width, height) for the sprite
        color: RGB tuple for the fairy's body color
        wing_color: RGB tuple for the wing color
        use_procedural: If True, generate procedural sprite; if False, try to load from assets
        asset_dir: Directory containing fairy assets
    
    Returns:
        pygame.Surface with the fairy sprite
    """
    if use_procedural:
        return create_procedural_fairy(size=size, color=color, wing_color=wing_color)
    else:
        asset_sprite = create_fairy_from_asset(name, size=size, asset_dir=asset_dir)
        # Fall back to procedural if asset not found
        if asset_sprite is None:
            print(f"Falling back to procedural sprite for: {name}")
            return create_procedural_fairy(size=size, color=color, wing_color=wing_color)
        return asset_sprite


def create_procedural_unicorn(size=(60, 60), color=(240, 240, 255), mane_color=(255, 105, 180), horn_color=(255, 215, 0)):
    """
    Creates a procedural unicorn sprite using pygame drawing primitives.
    
    Args:
        size: Tuple (width, height) for the sprite size
        color: RGB tuple for the unicorn's body color
        mane_color: RGB tuple for the mane and tail color
        horn_color: RGB tuple for the horn color
    
    Returns:
        pygame.Surface with the unicorn sprite drawn on it
    """
    width, height = size
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    center_x = width // 2
    center_y = height // 2
    
    # Body (ellipse)
    body_width = width // 2
    body_height = height // 3
    body_rect = pygame.Rect(
        center_x - body_width // 2,
        center_y + body_height // 4,
        body_width,
        body_height
    )
    pygame.draw.ellipse(surface, color, body_rect)
    
    # Neck and head
    neck_width = width // 6
    neck_height = height // 2
    neck_x = center_x + body_width // 4
    neck_y = center_y - neck_height // 4
    
    # Draw neck
    pygame.draw.polygon(
        surface,
        color,
        [
            (neck_x - neck_width // 2, center_y),
            (neck_x + neck_width // 2, center_y),
            (neck_x + neck_width // 3, neck_y - neck_height // 3),
            (neck_x - neck_width // 3, neck_y - neck_height // 3),
        ]
    )
    
    # Draw head (ellipse)
    head_width = neck_width
    head_height = neck_width * 2
    pygame.draw.ellipse(
        surface,
        color,
        (neck_x - head_width // 2, neck_y - head_height // 2, head_width, head_height)
    )
    
    # Draw horn (triangle)
    horn_base_width = neck_width // 2
    horn_height = height // 3
    horn_points = [
        (neck_x, neck_y - head_height // 2 - horn_height),  # Tip
        (neck_x - horn_base_width // 2, neck_y - head_height // 3),  # Left base
        (neck_x + horn_base_width // 2, neck_y - head_height // 3),  # Right base
    ]
    pygame.draw.polygon(surface, horn_color, horn_points)
    
    # Draw mane
    mane_points = [
        (neck_x - neck_width // 3, neck_y - neck_height // 4),
        (neck_x - neck_width, neck_y),
        (neck_x - neck_width // 2, center_y + body_height // 4),
    ]
    pygame.draw.polygon(surface, mane_color, mane_points)
    
    # Draw tail
    tail_start_x = center_x - body_width // 2
    tail_start_y = center_y + body_height // 2
    tail_points = [
        (tail_start_x, tail_start_y),
        (tail_start_x - width // 4, tail_start_y - height // 6),
        (tail_start_x - width // 5, tail_start_y),
        (tail_start_x - width // 4, tail_start_y + height // 6),
    ]
    pygame.draw.polygon(surface, mane_color, tail_points)
    
    # Draw legs
    leg_width = width // 10
    leg_height = height // 4
    
    # Front legs
    front_leg_x1 = center_x + body_width // 6
    front_leg_x2 = center_x + body_width // 3
    leg_y_start = center_y + body_height // 2
    
    pygame.draw.rect(surface, color, (front_leg_x1 - leg_width // 2, leg_y_start, leg_width, leg_height))
    pygame.draw.rect(surface, color, (front_leg_x2 - leg_width // 2, leg_y_start, leg_width, leg_height))
    
    # Back legs
    back_leg_x1 = center_x - body_width // 3
    back_leg_x2 = center_x - body_width // 6
    
    pygame.draw.rect(surface, color, (back_leg_x1 - leg_width // 2, leg_y_start, leg_width, leg_height))
    pygame.draw.rect(surface, color, (back_leg_x2 - leg_width // 2, leg_y_start, leg_width, leg_height))
    
    # Draw eye (small dot)
    eye_x = neck_x + head_width // 4
    eye_y = neck_y - head_height // 4
    eye_radius = 2
    pygame.draw.circle(surface, (0, 0, 0), (eye_x, eye_y), eye_radius)
    
    # Draw sparkles around horn
    sparkle_color = (*horn_color, 150)
    for i in range(3):
        sparkle_offset_x = (i - 1) * (width // 8)
        sparkle_y = neck_y - head_height // 2 - horn_height // 2
        sparkle_radius = 2 + i
        pygame.draw.circle(
            surface,
            sparkle_color,
            (neck_x + sparkle_offset_x, sparkle_y - (i + 1) * 3),
            sparkle_radius,
            1
        )
    
    return surface


def create_unicorn_from_asset(name: str, size=(60, 60), asset_dir="assets/unicorns"):
    """
    Loads a unicorn sprite from an asset file.
    
    Args:
        name: The unicorn's name (used to find the asset file)
        size: Tuple (width, height) to scale the sprite to
        asset_dir: Directory containing unicorn assets
    
    Returns:
        pygame.Surface with the loaded and scaled sprite, or None if not found
    """
    # Convert name to filename (e.g., "Star Dash" -> "star_dash.png")
    filename = name.lower().replace(" ", "_") + ".png"
    filepath = os.path.join(asset_dir, filename)
    
    if os.path.exists(filepath):
        try:
            sprite = pygame.image.load(filepath).convert_alpha()
            return pygame.transform.scale(sprite, size)
        except pygame.error:
            print(f"Warning: Failed to load unicorn asset: {filepath}")
            return None
    
    print(f"Warning: Unicorn asset not found: {filepath}")
    return None


def create_unicorn_sprite(name: str, size=(60, 60), color=(240, 240, 255), mane_color=(255, 105, 180), horn_color=(255, 215, 0), use_procedural=True, asset_dir="assets/unicorns"):
    """
    Creates a unicorn sprite, using procedural generation or assets based on the flag.
    
    Args:
        name: The unicorn's name (used to find asset files if not procedural)
        size: Tuple (width, height) for the sprite
        color: RGB tuple for the unicorn's body color
        mane_color: RGB tuple for the mane and tail color
        horn_color: RGB tuple for the horn color
        use_procedural: If True, generate procedural sprite; if False, try to load from assets
        asset_dir: Directory containing unicorn assets
    
    Returns:
        pygame.Surface with the unicorn sprite
    """
    if use_procedural:
        return create_procedural_unicorn(size=size, color=color, mane_color=mane_color, horn_color=horn_color)
    else:
        asset_sprite = create_unicorn_from_asset(name, size=size, asset_dir=asset_dir)
        # Fall back to procedural if asset not found
        if asset_sprite is None:
            print(f"Falling back to procedural sprite for: {name}")
            return create_procedural_unicorn(size=size, color=color, mane_color=mane_color, horn_color=horn_color)
        return asset_sprite
