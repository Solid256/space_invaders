import pygame
import sys
import random
from time import sleep
from bullet import Bullet
from alien import Alien
from saucer import Saucer
from pygame.sprite import Group
from barrier import Barrier


def check_events(game_running, stats, sb, ai_settings, screen, play_button, ship, aliens,
                 bullets, enemy_bullets, barriers, sprites):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():

        # If the event is QUIT, then exit the game.
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                              bullets, enemy_bullets, mouse_x, mouse_y, barriers, sprites)

        check_keydown_events(event, stats, ai_settings, screen, ship, bullets)
        check_keyup_events(event, stats, ai_settings, ship)

    return game_running


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,
                      enemy_bullets, mouse_x, mouse_y, barriers, sprites):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        enemy_bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens, sprites)
        create_barriers(ai_settings, screen, barriers, sprites )
        ship.center_ship()


def check_keydown_events(event, stats, ai_settings, screen, ship, bullets):
    # The keydown events.
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            # Allow the ship to move to the right.
            if not ai_settings.ship_destroyed:
                ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Allow the ship to move to the left.
            if not ai_settings.ship_destroyed:
                ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if stats.game_active:
                if not ai_settings.ship_destroyed:
                    ai_settings.firing_bullets = True
                    ai_settings.cur_frame_shoot = ai_settings.max_frame_shoot
        elif event.key == pygame.K_q:
            sys.exit()


def check_keyup_events(event, stats, ai_settings, ship):
    # The keyup events.
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            # Stop the ship from moving to the right.
            ship.moving_right = False
        if event.key == pygame.K_LEFT:
            # Stop the ship from moving to the left.
            ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            if stats.game_active:
                ai_settings.firing_bullets = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, barriers, play_button):
    """Update images on the screen and flip to the new screen."""
    # Primary game code.
    screen.fill(ai_settings.bg_color)

    # Draw the ship to the backbuffer.
    ship.blitme()

    # Redraw all the barriers.
    barriers.draw(screen)

    aliens.draw(screen)

    if not ai_settings.saucer == 0:
        ai_settings.saucer.blitme()

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bullet in enemy_bullets.sprites():
        bullet.draw_bullet()

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Swap the backbuffer.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets,
                   barriers, sprites):
    """Update position of bullets and get rid of old bullets."""

    # Fire bullets if firing bullets is enabled.
    if ai_settings.firing_bullets:

        ai_settings.cur_frame_shoot += ai_settings.speedup_scale

        while ai_settings.cur_frame_shoot > ai_settings.max_frame_shoot:
            fire_bullet(ai_settings, screen, ship, bullets)
            ai_settings.cur_frame_shoot -= ai_settings.max_frame_shoot
    else:
        ai_settings.cur_frame_shoot = 0.0

    # Updating the bullets.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

    # Check for any bullets that have hit barriers.
    # If so, get rid of the bullet and the barrier.
    check_bullet_barrier_collisions(ship, bullets, barriers)

    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets,
                                  enemy_bullets, barriers, sprites)


def update_enemy_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets,
                         barriers, sprites):
    """Update position of bullets and get rid of old bullets."""
    # Updating the bullets.
    enemy_bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in enemy_bullets.copy():
        if bullet.rect.bottom > 800:
            enemy_bullets.remove(bullet)
    # print(len(bullets))

    # Check for any bullets that have hit the player.
    # If so, get rid of the bullet and end the game.
    check_enemy_bullet_barrier_collisions(ship, enemy_bullets, barriers)

    # Check for any bullets that have hit the player.
    # If so, get rid of the bullet and end the game.
    check_enemy_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                       bullets, enemy_bullets, barriers, sprites)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets, enemy_bullets, barriers, sprites):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)

    if collisions:
        for alienGroup in collisions.values():
            stats.score += ai_settings.alien_points * len(alienGroup)
            sb.prep_score()

            for alien in alienGroup:
                alien.toggle_death = True
                alien.image = alien.image3

        check_high_score(stats, sb)
        pygame.mixer.Sound.play(ship.sound_blast)

    # Remove any bullets and saucers that have collided.
    if not ai_settings.saucer == 0:
        saucers = Group()
        saucers.add(ai_settings.saucer)

        collisions2 = pygame.sprite.groupcollide(bullets, saucers, True, False)

        for saucerGroup in collisions2.values():
            stats.score += ai_settings.alien_points * 10.0
            sb.prep_score()

            for saucer in saucerGroup:
                saucer.toggle_death = True
                saucer.image = saucer.image3

            check_high_score(stats, sb)
            pygame.mixer.Sound.play(ship.sound_blast)
            pygame.mixer.music.stop()

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        enemy_bullets.empty()
        ai_settings.increase_speed()
        ai_settings.saucer = 0
        ai_settings.cur_frame_saucer = 0

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens, sprites)
        create_barriers(ai_settings, screen, barriers, sprites)


def check_bullet_barrier_collisions(ship, bullets, barriers):
    """Respond to bullet-barrier collisions."""
    # Remove any bullets and barriers that have collided."""
    collisions = pygame.sprite.groupcollide(bullets, barriers, True, False)

    if collisions:
        for barrierGroup in collisions.values():

            for barrier in barrierGroup:
                barrier.health -= 1
                if barrier.health == 1:
                    barrier.image = barrier.image2
                elif barrier.health <= 0:
                    barriers.remove(barrier)

        pygame.mixer.Sound.play(ship.sound_blast)


def check_enemy_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets,
                                       enemy_bullets, barriers, sprites):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided."""
    player_group = Group()
    player_group.add(ship)

    collisions = pygame.sprite.groupcollide(enemy_bullets, player_group, True, False)

    if collisions:
        for shipGroup in collisions.values():
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets,
                     barriers, sprites, False)


def check_enemy_bullet_barrier_collisions(ship, enemy_bullets, barriers):
    """Respond to bullet-barrier collisions."""
    # Remove any bullets and barriers that have collided."""
    collisions = pygame.sprite.groupcollide(enemy_bullets, barriers, True, False)

    if collisions:
        for barrierGroup in collisions.values():

            for barrier in barrierGroup:
                barrier.health -= 1
                if barrier.health == 1:
                    barrier.image = barrier.image2
                elif barrier.health <= 0:
                    barriers.remove(barrier)

        pygame.mixer.Sound.play(ship.sound_blast)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship, None, 0)
        bullets.add(new_bullet)
        pygame.mixer.Sound.play(ship.sound_shot)


def fire_bullet_enemy(ai_settings, screen, ship, alien, enemy_bullets):
    """Fire a bullet if the limit is not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(enemy_bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, None, alien, 1)
        enemy_bullets.add(new_bullet)
        pygame.mixer.Sound.play(ship.sound_shot)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number, sprites):
    """Create an alien and place it in a row."""

    # The type of alien to create.
    alien_type = 3
    if row_number == 1 or row_number == 2:
        alien_type = 2
    elif row_number >= 3:
        alien_type = 1

    anim_toggle = False

    if (alien_number % 2) == 1:
        anim_toggle = True

    alien = Alien(ai_settings, screen, alien_type, anim_toggle, sprites)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.1 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.1 * alien.rect.height * row_number + 48
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, sprites):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen, 1, False, sprites)

    # The number of columns will be 11, just like in the original Space Invaders.
    number_aliens_x = 11

    # The number of rows will be 5, just like in the original Space Invaders.
    number_rows = 5

    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number, sprites)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    edge_detected = False

    for alien in aliens.sprites():
        if alien.check_edges():
            edge_detected = True
            change_fleet_direction(ai_settings, aliens)
            break

    if edge_detected:
        if ai_settings.fleet_direction == -1:
            for alien in aliens.sprites():
                alien.x -= 40
                alien.rect.x = alien.x
        else:
            for alien in aliens.sprites():
                alien.x += 40
                alien.rect.x = alien.x


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1


def create_barriers(ai_settings, screen, barriers, sprites):
    number_barriers_x = 4

    for x in range(0, number_barriers_x):
        barrier_offset_x = 160
        barrier_offset_y = 608

        barrier = Barrier(ai_settings, screen, barrier_offset_x + (256 * x),
                          barrier_offset_y, sprites, 1)
        barriers.add(barrier)
        barrier = Barrier(ai_settings, screen, barrier_offset_x + 32 + (256 * x),
                          barrier_offset_y, sprites, 0)
        barriers.add(barrier)
        barrier = Barrier(ai_settings, screen, barrier_offset_x + 64 + (256 * x),
                          barrier_offset_y, sprites, 0)
        barriers.add(barrier)
        barrier = Barrier(ai_settings, screen, barrier_offset_x + 96 + (256 * x),
                          barrier_offset_y, sprites, 2)
        barriers.add(barrier)
        barrier = Barrier(ai_settings, screen, barrier_offset_x + (256 * x),
                          barrier_offset_y + 32, sprites, 0)
        barriers.add(barrier)
        barrier = Barrier(ai_settings, screen, barrier_offset_x + 32 + (256 * x),
                          barrier_offset_y + 32, sprites, 4)
        barriers.add(barrier)
        barrier = Barrier(ai_settings, screen, barrier_offset_x + 64 + (256 * x),
                          barrier_offset_y + 32, sprites, 3)
        barriers.add(barrier)
        barrier = Barrier(ai_settings, screen, barrier_offset_x + 96 + (256 * x),
                          barrier_offset_y + 32, sprites, 0)
        barriers.add(barrier)
        barrier = Barrier(ai_settings, screen, barrier_offset_x + (256 * x),
                          barrier_offset_y + 64, sprites, 0)
        barriers.add(barrier)
        barrier = Barrier(ai_settings, screen, barrier_offset_x + 96 + (256 * x),
                          barrier_offset_y + 64, sprites, 0)
        barriers.add(barrier)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, barriers,
                  sprites):
    """Update the positions of all aliens in the fleet."""
    """
    Check if the fleet is at an edge, 
    and then update the positions of all aliens in the fleet.
    """
    for alien in aliens:
        if alien.dead:
            aliens.remove(alien)

    if not ai_settings.saucer == 0:
        if ai_settings.saucer.dead:
            ai_settings.saucer = 0

    # Update the enemy bullet chances.
    ai_settings.cur_frame_enemy_bullet += 0.5 * ai_settings.alien_speed_factor

    if ai_settings.cur_frame_enemy_bullet >= ai_settings.max_frame_enemy_bullet:
        ai_settings.cur_frame_enemy_bullet = 0.0
        num_aliens = len(aliens)

        if not num_aliens == 0:
            alien_index = random.randint(0, num_aliens-1)
            fire_bullet_enemy(ai_settings, screen, ship, aliens.sprites()[alien_index], enemy_bullets)

    aliens.update()
    check_fleet_edges(ai_settings, aliens)

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, barriers, False)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, barriers,
                        sprites)

    # Update the sound effects.

    # Update the sprite animation.
    ai_settings.cur_music_frame += 0.5 * ai_settings.alien_speed_factor

    while ai_settings.cur_music_frame > ai_settings.max_music_frames:
        ai_settings.cur_music_frame -= ai_settings.max_music_frames

    if ai_settings.cur_music_frame < 40.0:
        if ai_settings.cur_song == ai_settings.song4:
            ai_settings.cur_song = ai_settings.song1
            pygame.mixer.Sound.play(ai_settings.song1)
    elif 40.0 <= ai_settings.cur_music_frame < 80.0:
        if ai_settings.cur_song == ai_settings.song1:
            ai_settings.cur_song = ai_settings.song2
            pygame.mixer.Sound.play(ai_settings.song2)
    elif 80.0 <= ai_settings.cur_music_frame < 120.0:
        if ai_settings.cur_song == ai_settings.song2:
            ai_settings.cur_song = ai_settings.song3
            pygame.mixer.Sound.play(ai_settings.song3)
    elif ai_settings.cur_music_frame >= 120.0:
        if ai_settings.cur_song == ai_settings.song3:
            ai_settings.cur_song = ai_settings.song4
            pygame.mixer.Sound.play(ai_settings.song4)

    # Update the saucer controls.
    if not ai_settings.cur_frame_saucer < 0.0:
        ai_settings.cur_frame_saucer += 0.5 * ai_settings.alien_speed_factor

    if ai_settings.cur_frame_saucer > ai_settings.max_frame_saucer:
        ai_settings.saucer = Saucer(ai_settings, screen, sprites)
        ai_settings.cur_frame_saucer = -1.0

        ai_settings.saucer.x = 0
        ai_settings.saucer.y = 128

    if not ai_settings.saucer == 0:
        ai_settings.saucer.update()


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets,
             barriers, sprites, pause):
    """Respond to ship being hit by alien."""
    # Decrement ships_left.
    stats.ships_left -= 1

    # Update scoreboard.
    sb.prep_ships()

    ai_settings.ship_destroyed = True

    # Pause.
    if pause:
        sleep(0.5)
        end_level(ai_settings, screen, stats, ship, aliens, bullets, enemy_bullets, barriers, sprites)
    else:
        pygame.mixer.Sound.play(ship.sound_ship_destroyed)


def end_level(ai_settings, screen, stats, ship, aliens, bullets, enemy_bullets, barriers, sprites):
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    enemy_bullets.empty()
    barriers.empty()
    ai_settings.saucer = 0
    ai_settings.cur_frame_saucer = 0
    ai_settings.cur_frame_ship_destroyed = 0.0
    ai_settings.ship_destroyed = False
    ai_settings.end_level = False

    pygame.mixer.music.stop()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens, sprites)
    create_barriers(ai_settings, screen, barriers, sprites)
    ship.center_ship()

    if stats.ships_left < 0:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets,
                        barriers, sprites):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, barriers,
                     sprites, True)
            break


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
