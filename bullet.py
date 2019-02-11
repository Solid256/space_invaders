import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    def __init__(self, ai_settings, screen, ship, alien, bullet_type):
        """Create a bullet object at the ship's current position."""
        super(Bullet, self).__init__()
        self.screen = screen
        self.bullet_type = bullet_type

        if bullet_type == 0:
            # Create a bullet rect at (0, 0) and then set correct position.
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
            self.rect.centerx = ship.rect.centerx
            self.rect.top = ship.rect.top

            self.color = ai_settings.bullet_color
            self.speed_factor = ai_settings.bullet_speed_factor

        else:
            # Create a bullet rect at (0, 0) and then set correct position.
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
            self.rect.centerx = alien.rect.centerx
            self.rect.top = alien.rect.top

            self.color = ai_settings.enemy_bullet_color
            self.speed_factor = ai_settings.bullet_speed_factor

        if self.speed_factor > ai_settings.max_bullet_speed_factor:
            self.speed_factor = ai_settings.max_bullet_speed_factor

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        if self.bullet_type == 0:
            # Update the decimal position of the bullet.
            self.y -= self.speed_factor
        else:
            # Update the decimal position of the bullet.
            self.y += 0.5 * self.speed_factor

        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    # Member variables:
    speed_factor = 0.0
