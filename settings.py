import pygame


class Settings:
    """A class to store all settings for the game Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings:
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 180, 180, 180
        self.bullets_allowed = 3
        self.enemy_bullet_color = 250, 60, 80
        self.cur_frame_shoot = 0.0
        self.max_frame_shoot = 10
        self.firing_bullets = False
        self.max_bullet_speed_factor = 20

        # Alien settings:
        self.fleet_drop_speed = 16

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # The initial music frames.
        self.cur_music_frame = 0.0
        self.max_music_frames = 160.0

        # The initial sound effects.
        self.song1 = pygame.mixer.Sound("audio/space_invaders_song_1.wav")
        self.song2 = pygame.mixer.Sound("audio/space_invaders_song_2.wav")
        self.song3 = pygame.mixer.Sound("audio/space_invaders_song_3.wav")
        self.song4 = pygame.mixer.Sound("audio/space_invaders_song_4.wav")

        self.cur_song = self.song4

        # The time constraints for the saucer ship.
        self.cur_frame_saucer = 0
        self.max_frame_saucer = 400
        self.saucer = 0

        # The enemy bullet class.
        self.cur_frame_enemy_bullet = 0
        self.max_frame_enemy_bullet = 40

        self.ship_destroyed = False
        self.cur_frame_ship_destroyed = 0.0
        self.max_frame_ship_destroyed = 20.0

        self.end_level = False

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 3.0
        self.bullet_speed_factor = 8
        self.alien_speed_factor = 2
        self.max_bullet_speed_factor = 20

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring.
        self.alien_points = 50

        self.cur_music_frame = 0.0
        self.max_music_frames = 160.0
        self.cur_song = self.song4

        self.cur_frame_saucer = 0
        self.saucer = 0
        self.cur_frame_shoot = 0
        self.firing_bullets = False

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

        self.cur_frame_saucer = 0
        self.saucer = 0

    # Member variables.

    # Ship, bullet and alien speed factors.
    ship_speed_factor = 3.0
    bullet_speed_factor = 8
    alien_speed_factor = 2

    # fleet_direction of 1 represents right; -1 represents left.
    fleet_direction = 1

    # Scoring.
    alien_points = 50