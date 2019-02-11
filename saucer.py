import pygame
from pygame.sprite import Sprite


class Saucer(Sprite):
    """A class to represent a single alien in t he fleet."""

    def __init__(self, ai_settings, screen, sprites):
        """Initialize the alien and set its starting position."""
        super(Saucer, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.max_frames = 80.0
        self.cur_frame = 0.0
        self.move_toggle1 = True
        self.toggle_death = False
        self.dead = False

        sprite_info = sprites.sprite_infos["invader4_1.png"]
        self.image = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["invader4_2.png"]
        self.image2 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        sprite_info = sprites.sprite_infos["invader_death_2.png"]
        self.image3 = sprites.sprite_sheet.subsurface(
            pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        self.image1 = self.image
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

        # The saucer song.
        self.saucer_song = pygame.mixer.music.load("audio/saucer.wav")
        pygame.mixer.music.play(-1)

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right."""

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            pygame.mixer.music.stop()
            self.dead = True

        if self.toggle_death:
            self.dead = True
        else:
            # Update the sprite animation.
            self.cur_frame += 2.0 * self.ai_settings.alien_speed_factor

            self.x += 2.0 * self.ai_settings.alien_speed_factor
            self.rect.x = self.x

            while self.cur_frame > self.max_frames:
                self.cur_frame -= self.max_frames

            if self.cur_frame < 40.0:
                self.image = self.image1
            elif self.cur_frame >= 40.0:
                self.image = self.image2
