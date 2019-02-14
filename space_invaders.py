import sys
import pygame
import random

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sprites import Sprites

import game_functions as gf


# This function starts off the Space invaders game.
def run_game():
    # Create the pygame module.
    pygame.init()

    # Get the pygame clock.
    pygame_clock = pygame.time.Clock()

    # Initialize the random seed.
    random.seed()

    # Create the game settings.
    ai_settings = Settings()

    # The backbuffer of the game.
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")

    # Make the sprite loader object.
    sprites = Sprites()

    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)

    # Create the scoreboard.
    sb = Scoreboard(ai_settings, screen, stats, sprites)

    # Checks if the game is currently running.
    game_running = True

    # Make a group to store bullets in.
    bullets = Group()

    # Make a group to store enemy bullets in.
    enemy_bullets = Group()

    # Make a group to store the aliens in.
    aliens = Group()

    # Make a group to store the barriers in.
    barriers = Group()

    # Make the Space text.
    space_text = None

    # Make the Invaders text.
    invaders_text = None

    # Make the high scores text.
    high_scores_text = None

    while game_running:
        if ai_settings.current_sequence == 0:
            # Make the Play button.
            if ai_settings.play_button is None:
                ai_settings.play_button = Button(ai_settings, screen, 600, (128, 255, 128), "PLAY GAME")

            # Make the Play button.
            if ai_settings.high_scores_button is None:
                ai_settings.high_scores_button = Button(ai_settings, screen, 664, (128, 128, 128), "HIGH SCORES")

            # Make the Space text.
            if space_text is None:
                cur_font = pygame.font.Font("fonts/BPdotsPlusBold.otf", 128)

                # Build the button's rect object and center it.
                space_text = cur_font.render("SPACE", True, (255, 255, 255), (0, 0, 0))

            # Make the Invaders text.
            if invaders_text is None:
                cur_font = pygame.font.Font("fonts/BPdotsPlusBold.otf", 64)

                # Build the button's rect object and center it.
                invaders_text = cur_font.render("INVADERS", True, (128, 255, 128), (0, 0, 0))

        elif ai_settings.current_sequence == 1:

            if ai_settings.ship is None:
                # Make a ship
                ai_settings.ship = Ship(screen, ai_settings, sprites)
                ai_settings.ship.center_ship()

            if stats.game_active and game_running:
                # Updating the game objects.
                ai_settings.ship.update()

                # Check if the level needs to be ended.
                if ai_settings.end_level:
                    gf.end_level(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets,
                                 barriers, sprites)

                if not ai_settings.ship_destroyed and ai_settings.ship is not None:
                    gf.update_bullets(ai_settings, screen, stats, sb, aliens, bullets,
                                      enemy_bullets, barriers, sprites)
                    gf.update_enemy_bullets(ai_settings, screen, stats, sb, aliens, bullets,
                                            enemy_bullets, barriers, sprites)
                    gf.update_aliens(ai_settings, screen, stats, sb, aliens, bullets,
                                     enemy_bullets, barriers, sprites)

        elif ai_settings.current_sequence == 3:
            # Make the Invaders text.
            if high_scores_text is None:
                cur_font = pygame.font.Font("fonts/BPdotsPlusBold.otf", 64)

                # Build the button's rect object and center it.
                high_scores_text = cur_font.render("HIGH SCORES", True, (128, 255, 128), (0, 0, 0))

            # Make the high scores back button.
            if ai_settings.high_scores_back_button is None:
                ai_settings.high_scores_back_button = Button(ai_settings, screen, 664, (128, 128, 128), "BACK")

        # Updating the rendering process.
        gf.update_screen(ai_settings, screen, stats, sb, aliens, bullets,
                         enemy_bullets, barriers, space_text, invaders_text, high_scores_text, sprites)

        # Checking for game events.
        game_running = gf.check_events(game_running, stats, sb, ai_settings, screen, aliens, bullets,
                                       enemy_bullets, barriers, sprites)

        pygame_clock.tick(60)

    # Exit pygame.
    pygame.quit()

    # Quit the program.
    sys.exit()


run_game()
