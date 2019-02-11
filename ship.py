import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, screen, ai_settings, sprites):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        sprite_info = sprites.sprite_infos["ship.png"]
        self.image1 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["ship_death_1.png"]
        self.image2 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["ship_death_2.png"]
        self.image3 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["ship_death_3.png"]
        self.image4 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["ship_death_4.png"]
        self.image5 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["ship_death_5.png"]
        self.image6 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["ship_death_6.png"]
        self.image7 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["ship_death_7.png"]
        self.image8 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["ship_death_8.png"]
        self.image9 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        self.image = self.image1

        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flags.
        self.moving_right = False
        self.moving_left = False

        # Sound effects.
        self.sound_shot = pygame.mixer.Sound("audio/shot_1.wav")
        self.sound_blast = pygame.mixer.Sound("audio/blast_1.wav")
        self.sound_ship_destroyed = pygame.mixer.Sound("audio/ship_destroyed.wav")

        # Death animation.
        self.cur_frame_death = 0.0
        self.max_frame_death = 20.0

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flag."""
        if not self.ai_settings.ship_destroyed:
            self.image = self.image1
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor

            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor

            # Update rect object from self.center.
            self.rect.centerx = self.center
        else:
            if self.cur_frame_death == 0.0:
                self.image = self.image2
                self.rect.centery -= 48

            self.cur_frame_death += 1

            self.ai_settings.firing_bullets = False

            if self.cur_frame_death == 2.0:
                self.image = self.image3
            elif self.cur_frame_death == 4.0:
                self.image = self.image4
            elif self.cur_frame_death == 6.0:
                self.image = self.image5
            elif self.cur_frame_death == 8.0:
                self.image = self.image6
            elif self.cur_frame_death == 10.0:
                self.image = self.image7
            elif self.cur_frame_death == 12.0:
                self.image = self.image8
            elif self.cur_frame_death == 14.0:
                self.image = self.image9

            # Check when to restart the level or end the game.
            self.ai_settings.cur_frame_ship_destroyed += 1

            if self.ai_settings.cur_frame_ship_destroyed > self.ai_settings.max_frame_ship_destroyed:
                self.rect.centery += 48
                self.ai_settings.end_level = True
                self.cur_frame_death = 0.0
                self.ai_settings.ship_destroyed = False

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
        self.image = self.image1
