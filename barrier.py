import pygame
from pygame.sprite import Sprite


class Barrier(Sprite):
    def __init__(self, ai_settings, screen, position_x, position_y, sprites, barrier_type):
        super(Barrier, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.health = 2

        # The barrier type. Type:
        # 0 - square.
        # 1 - Top left.
        # 2 - Top right.
        # 3 - Bottom left.
        # 4 - Bottom right.
        self.barrier_type = barrier_type

        if self.barrier_type == 0:
            sprite_info = sprites.sprite_infos["wall1_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            sprite_info = sprites.sprite_infos["wall1_2.png"]
            self.image2 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        elif self.barrier_type == 1:
            sprite_info = sprites.sprite_infos["wall1TL_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            sprite_info = sprites.sprite_infos["wall1TL_2.png"]
            self.image2 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        elif self.barrier_type == 2:
            sprite_info = sprites.sprite_infos["wall1TR_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            sprite_info = sprites.sprite_infos["wall1TR_2.png"]
            self.image2 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        elif self.barrier_type == 3:
            sprite_info = sprites.sprite_infos["wall1BL_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            sprite_info = sprites.sprite_infos["wall1BL_2.png"]
            self.image2 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        elif self.barrier_type == 4:
            sprite_info = sprites.sprite_infos["wall1BR_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            sprite_info = sprites.sprite_infos["wall1BR_2.png"]
            self.image2 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        self.image = self.image1

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = position_x
        self.rect.y = position_y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the barrier at its current location"""
        self.screen.blit(self.image, self.rect)