import pygame
import random

from pygame.sprite import Sprite
from PIL import Image


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

        self.image2PIL = Image.new("RGB", (32, 32), color="black")
        self.image2 = pygame.Surface((32, 32), )

        if self.barrier_type == 0:
            sprite_info = sprites.sprite_infos["wall1_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        elif self.barrier_type == 1:
            sprite_info = sprites.sprite_infos["wall1TL_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        elif self.barrier_type == 2:
            sprite_info = sprites.sprite_infos["wall1TR_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        elif self.barrier_type == 3:
            sprite_info = sprites.sprite_infos["wall1BL_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        elif self.barrier_type == 4:
            sprite_info = sprites.sprite_infos["wall1BR_1.png"]
            self.image1 = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

        self.image = self.image1

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = position_x
        self.rect.y = position_y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update_image_pixels(self):
        # The pygame pixel array.
        pixel_array = pygame.PixelArray(self.image1)

        # The pygame pixel array for the second texture.
        pixel_array2 = pygame.PixelArray(self.image2)

        # The Pillow pixel array.
        pixels = self.image2PIL.load()

        # Copy the pixels from the pygame texture to the pillow texture.
        for pixelX in range(0, 32):
            for pixelY in range(0, 32):
                color = pixel_array[pixelX, pixelY]

                pixels[pixelX, pixelY] = color

        # Choose which pixels should be black.
        for pixelX in range(0, 32):
            for pixelY in range(0, 32):
                # Checks randomly if the pixel should be colored black.
                dist_from_center = int(pow((pow(pixelX - 16, 2) + pow(pixelY - 16, 2)), 0.5))

                black_or_green_num = random.randint(0, int(pow(dist_from_center / 1.5, 2)))

                if black_or_green_num < 16:
                    black_or_green = True
                else:
                    black_or_green = False

                if black_or_green:
                    pixels[pixelX, pixelY] = (0, 0, 0)

        # Copy the pixels from the pillow texture to the pygame texture.
        for pixelX in range(0, 32):
            for pixelY in range(0, 32):
                color = pixels[pixelX, pixelY]

                pixel_array2[pixelX, pixelY] = color

        self.image = self.image2

    def blitme(self):
        """Draw the barrier at its current location"""
        self.screen.blit(self.image, self.rect)
