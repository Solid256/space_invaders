import pygame.font
from pygame.sprite import Group

from ship import Ship

import struct


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats, sprites):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.sprites = sprites

        # Font settings for scoring information.
        self.text_color = (230, 230, 230)
        self.font = pygame.font.Font("fonts/BPdotsPlusBold.otf", 48)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.high_scores = []

        in_file = open("high_scores.bin", "rb")

        for x in range(0, 10):
            cur_score = struct.unpack('i', in_file.read(4))[0]
            self.high_scores.append(cur_score)

        in_file.close()

        self.stats.high_score = self.high_scores[0]

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw scores and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw ships.
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))

        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.screen, self.ai_settings, self.sprites)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def add_new_high_score(self, high_score):

        # Add the new high score by comparing to other high scores.
        for x in range(0, len(self.high_scores)):
            if high_score >= self.high_scores[x]:
                self.high_scores.insert(x, high_score)
                self.high_scores.pop(9)
                break

    def export_new_high_scores(self):

        # The out file for the high scores.
        out_file = open("high_scores.bin", "wb")

        for x in range(0, 10):
            cur_score = struct.pack('i', self.high_scores[x])
            out_file.write(cur_score)

        out_file.close()

    # Member variables:
    score_image = None
    score_rect = None
    high_score_image = None
    high_score_rect = None
    level_image = None
    level_rect = None
    ships = None
