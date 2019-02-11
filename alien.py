import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in t he fleet."""

    def __init__(self, ai_settings, screen, alien_type, anim_toggle, sprites):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.alien_type = alien_type
        self.max_frames = 80.0
        self.cur_frame = 0.0
        self.move_toggle1  = False
        self.anim_toggle = anim_toggle
        self.toggle_death = False
        self.dead = False

        # Load the alien image and set its rect attribute.
        if alien_type == 1:
            sprite_info = sprites.sprite_infos["invader1_1.png"]
            self.image = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            sprite_info = sprites.sprite_infos["invader1_2.png"]
            self.image2 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))
        elif alien_type == 2:
            sprite_info = sprites.sprite_infos["invader2_1.png"]
            self.image = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            sprite_info = sprites.sprite_infos["invader2_2.png"]
            self.image2 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))
        elif alien_type == 3:
            sprite_info = sprites.sprite_infos["invader3_1.png"]
            self.image = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            sprite_info = sprites.sprite_infos["invader3_2.png"]
            self.image2 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["invader_death_1_1.png"]
        self.image3 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["invader_death_1_2.png"]
        self.image4 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["invader_death_1_3.png"]
        self.image5 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        self.image1 = self.image
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right."""

        if self.toggle_death:
            if self.max_frames == 80.0:
                self.max_frames = 6.0
                self.cur_frame = 0.0
                self.image = self.image3
            else:
                self.cur_frame += 1.0

                if self.cur_frame == 2.0:
                    self.image = self.image4
                elif self.cur_frame == 4.0:
                    self.image = self.image5
                elif self.cur_frame == self.max_frames:
                    self.dead = True
        else:
            # Update the sprite animation.
            self.cur_frame += 0.5 * self.ai_settings.alien_speed_factor

            while self.cur_frame > self.max_frames:
                self.cur_frame -= self.max_frames

            if self.cur_frame < 40.0:
                if self.move_toggle1:
                    self.x += 40 * self.ai_settings.fleet_direction
                    self.rect.x = self.x
                    self.move_toggle1 = False

                    if not self.anim_toggle:
                        self.image = self.image1
                        self.anim_toggle = True
                    else:
                        self.image = self.image2
                        self.anim_toggle = False
            elif self.cur_frame >= 40.0:
                if not self.move_toggle1:
                    self.x += 40 * self.ai_settings.fleet_direction
                    self.rect.x = self.x
                    self.move_toggle1 = True

                    if self.anim_toggle:
                        self.image = self.image2
                        self.anim_toggle = False
                    else:
                        self.image = self.image1
                        self.anim_toggle = True
