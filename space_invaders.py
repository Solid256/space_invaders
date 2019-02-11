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

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)

    # Create the scoreboard.
    sb = Scoreboard(ai_settings, screen, stats, sprites)

    # Make a ship
    ship = Ship(screen, ai_settings, sprites)

    # Make a group to store bullets in.
    bullets = Group()

    # Make a group to store enemy bullets in.
    enemy_bullets = Group()

    # Make a group to store the aliens in.
    aliens = Group()

    # Make a group to store the barriers in.
    barriers = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens, sprites)

    # Create the barriers.
    gf.create_barriers(ai_settings, screen, barriers, sprites)

    # Checks if the game is currently running.
    game_running = True

    # The main game loop.
    while game_running:

        # Checking for game events.
        game_running = gf.check_events(game_running, stats, sb, ai_settings, screen,
                                       play_button, ship, aliens, bullets, enemy_bullets,
                                       barriers, sprites)

        if stats.game_active and game_running:
            # Updating the game objects.
            ship.update()

            # Check if the level needs to be ended.
            if ai_settings.end_level:
                gf.end_level(ai_settings, screen, stats, ship, aliens, bullets, enemy_bullets,
                             barriers, sprites)

            if not ai_settings.ship_destroyed:
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,
                                  enemy_bullets, barriers, sprites)
                gf.update_enemy_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,
                                        enemy_bullets, barriers, sprites)
                gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets,
                                 enemy_bullets, barriers, sprites)

        if game_running:
            # Updating the rendering process.
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                             enemy_bullets, barriers, play_button)

        pygame_clock.tick(60)

    # Exit pygame.
    pygame.quit()

    # Quit the program.
    sys.exit()


run_game()
