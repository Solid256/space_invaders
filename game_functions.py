import pygame
import sys
import random
from time import sleep
from bullet import Bullet
from alien import Alien
from saucer import Saucer
from pygame.sprite import Group
from barrier import Barrier


def check_events(game_running, stats, sb, ai_settings, screen, aliens,
                 bullets, enemy_bullets, barriers, sprites):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():

        # If the event is QUIT, then exit the game.
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if ai_settings.play_button is not None:
                check_play_button(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets, mouse_x,
                                  mouse_y, barriers, sprites)

            if ai_settings.high_scores_button is not None:
                check_high_scores_button(ai_settings, stats, mouse_x, mouse_y)

            if ai_settings.high_scores_back_button is not None:
                check_high_scores_back_button(ai_settings, stats, mouse_x, mouse_y)

        check_keydown_events(event, stats, ai_settings)
        check_keyup_events(event, stats, ai_settings)

    return game_running


def check_play_button(ai_settings, screen, stats, sb, aliens, bullets,
                      enemy_bullets, mouse_x, mouse_y, barriers, sprites):
    """Start a new game when the player clicks Play."""
    button_clicked = ai_settings.play_button.rect.collidepoint(mouse_x, mouse_y)
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
        create_fleet(ai_settings, screen, aliens, sprites)
        create_barriers(ai_settings, screen, barriers, sprites)

        del ai_settings.play_button
        del ai_settings.high_scores_button

        ai_settings.play_button = None
        ai_settings.high_scores_button = None

        ai_settings.current_sequence = 1


def check_high_scores_button(ai_settings, stats, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = ai_settings.high_scores_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        del ai_settings.high_scores_button
        del ai_settings.play_button

        ai_settings.play_button = None
        ai_settings.high_scores_button = None

        ai_settings.current_sequence = 3


def check_high_scores_back_button(ai_settings, stats, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = ai_settings.high_scores_back_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        del ai_settings.high_scores_back_button

        ai_settings.high_scores_back_button = None

        ai_settings.current_sequence = 0


def check_keydown_events(event, stats, ai_settings):
    # The keydown events.
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            # Allow the ship to move to the right.
            if not ai_settings.ship_destroyed and ai_settings.current_sequence == 1:
                ai_settings.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Allow the ship to move to the left.
            if not ai_settings.ship_destroyed and ai_settings.current_sequence == 1:
                ai_settings.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if stats.game_active:
                if not ai_settings.ship_destroyed and ai_settings.current_sequence == 1:
                    ai_settings.firing_bullets = True
                    ai_settings.cur_frame_shoot = ai_settings.max_frame_shoot
        elif event.key == pygame.K_q:
            sys.exit()


def check_keyup_events(event, stats, ai_settings):
    # The keyup events.
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            # Stop the ship from moving to the right.
            if ai_settings.current_sequence == 1:
                ai_settings.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            # Stop the ship from moving to the left.
            if ai_settings.current_sequence == 1:
                ai_settings.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            if stats.game_active:
                ai_settings.firing_bullets = False


def update_screen(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets, barriers, space_text,
                  invaders_text, high_scores_text, sprites):
    """Update images on the screen and flip to the new screen."""
    # Primary game code.
    screen.fill(ai_settings.bg_color)

    if ai_settings.current_sequence == 0:
        # Draw the play button if the game is inactive.
        if not stats.game_active:
            if ai_settings.play_button is not None:
                ai_settings.play_button.draw_button()
            if ai_settings.high_scores_button is not None:
                ai_settings.high_scores_button.draw_button()

            # Render the alien invaders text.
            msg_image_rect = space_text.get_rect()
            msg_image_rect.centerx = screen.get_rect().centerx
            msg_image_rect.centery = 128
            screen.blit(space_text, msg_image_rect)

            msg_image_rect = invaders_text.get_rect()
            msg_image_rect.centerx = screen.get_rect().centerx
            msg_image_rect.centery = 220
            screen.blit(invaders_text, msg_image_rect)

            # Render the four alien types.
            sprite_info = sprites.sprite_infos["invader1_1.png"]
            cur_image = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            cur_rect = cur_image.get_rect()
            cur_rect.centerx = screen.get_rect().centerx - 120
            cur_rect.centery = 300

            screen.blit(cur_image, cur_rect)

            sprite_info = sprites.sprite_infos["invader2_1.png"]
            cur_image = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            cur_rect = cur_image.get_rect()
            cur_rect.centerx = screen.get_rect().centerx - 120
            cur_rect.centery = 364

            screen.blit(cur_image, cur_rect)

            sprite_info = sprites.sprite_infos["invader3_1.png"]
            cur_image = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            cur_rect = cur_image.get_rect()
            cur_rect.centerx = screen.get_rect().centerx - 120
            cur_rect.centery = 428

            screen.blit(cur_image, cur_rect)

            sprite_info = sprites.sprite_infos["invader4_1.png"]
            cur_image = sprites.sprite_sheet.subsurface(
                pygame.Rect(sprite_info.x, sprite_info.y, sprite_info.w, sprite_info.h))

            cur_rect = cur_image.get_rect()
            cur_rect.centerx = screen.get_rect().centerx - 120
            cur_rect.centery = 472

            screen.blit(cur_image, cur_rect)

            # Render the alien values text.
            cur_font = pygame.font.Font("fonts/BPdotsPlusBold.otf", 32)

            # Build the text's rect object and center it.
            invaders_text = cur_font.render("= 10 PTS", True, (200, 200, 200), (0, 0, 0))

            msg_image_rect = invaders_text.get_rect()
            msg_image_rect.centerx = screen.get_rect().centerx + 10
            msg_image_rect.centery = 300
            screen.blit(invaders_text, msg_image_rect)

            invaders_text = cur_font.render("= 20 PTS", True, (200, 200, 200), (0, 0, 0))

            msg_image_rect = invaders_text.get_rect()
            msg_image_rect.centerx = screen.get_rect().centerx + 10
            msg_image_rect.centery = 364
            screen.blit(invaders_text, msg_image_rect)

            invaders_text = cur_font.render("= 40 PTS", True, (200, 200, 200), (0, 0, 0))

            msg_image_rect = invaders_text.get_rect()
            msg_image_rect.centerx = screen.get_rect().centerx + 10
            msg_image_rect.centery = 428
            screen.blit(invaders_text, msg_image_rect)

            invaders_text = cur_font.render("= ???", True, (200, 200, 200), (0, 0, 0))

            msg_image_rect = invaders_text.get_rect()
            msg_image_rect.centerx = screen.get_rect().centerx + 10
            msg_image_rect.centery = 490
            screen.blit(invaders_text, msg_image_rect)
    elif ai_settings.current_sequence == 1:
        # Draw the ship to the backbuffer.
        ai_settings.ship.blitme()

        # Redraw all the barriers.
        barriers.draw(screen)

        aliens.draw(screen)

        if ai_settings.saucer is not None:
            ai_settings.saucer.blitme()

        # Redraw all bullets behind ship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        for bullet in enemy_bullets.sprites():
            bullet.draw_bullet()

        # Draw the score information.
        sb.show_score()
    elif ai_settings.current_sequence == 3:
        # Render the high score text.
        msg_image_rect = high_scores_text.get_rect()
        msg_image_rect.centerx = screen.get_rect().centerx
        msg_image_rect.centery = 100
        screen.blit(high_scores_text, msg_image_rect)

        # Render the back button.
        if ai_settings.high_scores_back_button is not None:
            ai_settings.high_scores_back_button.draw_button()

        high_scores = sb.high_scores

        text_y_offset = 200

        for high_score in high_scores:
            # Render the high scores values text.
            cur_font = pygame.font.Font("fonts/BPdotsPlusBold.otf", 32)

            invaders_text = cur_font.render(str(high_score), True, (200, 200, 200), (0, 0, 0))

            msg_image_rect = invaders_text.get_rect()
            msg_image_rect.centerx = screen.get_rect().centerx + 10
            msg_image_rect.centery = text_y_offset
            screen.blit(invaders_text, msg_image_rect)

            text_y_offset += 40

    # Swap the backbuffer.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets,
                   barriers, sprites):
    """Update position of bullets and get rid of old bullets."""

    # Fire bullets if firing bullets is enabled.
    if ai_settings.firing_bullets:

        ai_settings.cur_frame_shoot += ai_settings.speedup_scale

        while ai_settings.cur_frame_shoot > ai_settings.max_frame_shoot:
            fire_bullet(ai_settings, screen, bullets)
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
    check_bullet_barrier_collisions(ai_settings, bullets, barriers)

    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, aliens, bullets,
                                  enemy_bullets, barriers, sprites)


def update_enemy_bullets(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets,
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
    check_enemy_bullet_barrier_collisions(ai_settings, enemy_bullets, barriers)

    # Check for any bullets that have hit the player.
    # If so, get rid of the bullet and end the game.
    check_enemy_bullet_ship_collisions(ai_settings, screen, stats, sb, aliens,
                                       bullets, enemy_bullets, barriers, sprites)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, aliens,
                                  bullets, enemy_bullets, barriers, sprites):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)

    if collisions:
        for alienGroup in collisions.values():
            for cur_alien in alienGroup:
                if cur_alien.alien_type == 1:
                    stats.score += 10
                elif cur_alien.alien_type == 2:
                    stats.score += 20
                elif cur_alien.alien_type == 3:
                    stats.score += 40

            sb.prep_score()

            for alien in alienGroup:
                alien.toggle_death = True
                alien.image = alien.image3
                ai_settings.increase_speed()

        check_high_score(stats, sb)
        pygame.mixer.Sound.play(ai_settings.ship.sound_blast)

    # Remove any bullets and saucers that have collided.
    if ai_settings.saucer is not None:
        saucers = Group()
        saucers.add(ai_settings.saucer)

        collisions2 = pygame.sprite.groupcollide(bullets, saucers, True, False)

        for saucerGroup in collisions2.values():
            stats.score += ai_settings.alien_points * 10.0
            sb.prep_score()

            for saucer in saucerGroup:
                saucer.toggle_death = True

            check_high_score(stats, sb)
            pygame.mixer.Sound.play(ai_settings.ship.sound_blast)
            pygame.mixer.music.stop()

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        enemy_bullets.empty()
        del ai_settings.saucer
        ai_settings.saucer = None
        ai_settings.cur_frame_saucer = 0
        ai_settings.initialize_dynamic_settings()
        ai_settings.speedup_scale += 0.005

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, aliens, sprites)
        create_barriers(ai_settings, screen, barriers, sprites)


def check_bullet_barrier_collisions(ai_settings, bullets, barriers):
    """Respond to bullet-barrier collisions."""
    # Remove any bullets and barriers that have collided."""
    collisions = pygame.sprite.groupcollide(bullets, barriers, True, False)

    if collisions:
        for barrierGroup in collisions.values():

            for barrier in barrierGroup:
                barrier.health -= 1
                if barrier.health == 1:
                    barrier.update_image_pixels()
                elif barrier.health <= 0:
                    barriers.remove(barrier)

        pygame.mixer.Sound.play(ai_settings.ship.sound_blast)


def check_enemy_bullet_ship_collisions(ai_settings, screen, stats, sb, aliens, bullets,
                                       enemy_bullets, barriers, sprites):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    if ai_settings.ship is not None:
        player_group = Group()
        player_group.add(ai_settings.ship)

        collisions = pygame.sprite.groupcollide(enemy_bullets, player_group, True, False)

        if collisions:
            for x in range(0, len(collisions.values())):
                ship_hit(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets,
                         barriers, sprites, False)


def check_enemy_bullet_barrier_collisions(ai_settings, enemy_bullets, barriers):
    """Respond to bullet-barrier collisions."""
    # Remove any bullets and barriers that have collided."""
    collisions = pygame.sprite.groupcollide(enemy_bullets, barriers, True, False)

    if collisions:
        for barrierGroup in collisions.values():

            for barrier in barrierGroup:
                barrier.health -= 1
                if barrier.health == 1:
                    barrier.update_image_pixels()
                elif barrier.health <= 0:
                    barriers.remove(barrier)

        pygame.mixer.Sound.play(ai_settings.ship.sound_blast)


def fire_bullet(ai_settings, screen, bullets):
    """Fire a bullet if limit not reached yet"""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, None, 0)
        bullets.add(new_bullet)
        pygame.mixer.Sound.play(ai_settings.ship.sound_shot)


def fire_bullet_enemy(ai_settings, screen, alien, enemy_bullets):
    """Fire a bullet if the limit is not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(enemy_bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, alien, 1)
        enemy_bullets.add(new_bullet)

        if ai_settings.ship is not None:
            pygame.mixer.Sound.play(ai_settings.ship.sound_shot)


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
    if row_number == 2 or row_number == 3:
        alien_type = 2
    elif row_number >= 4:
        alien_type = 1

    anim_toggle = False

    if (alien_number % 2) == 1:
        anim_toggle = True

    alien = Alien(ai_settings, screen, alien_type, anim_toggle, sprites)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.1 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.0 * alien.rect.height * row_number + 48
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, sprites):
    """Create a full fleet of aliens."""
    # Spacing between each alien is manually selected to be short.

    # The number of columns will be 11, just like in the original Space Invaders.
    number_aliens_x = 11

    # The number of rows will be 6.
    number_rows = 6

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


def update_aliens(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets, barriers,
                  sprites):
    """Update the positions of all aliens in the fleet."""
    """
    Check if the fleet is at an edge, 
    and then update the positions of all aliens in the fleet.
    """
    for alien in aliens:
        if alien.dead:
            aliens.remove(alien)

    if ai_settings.saucer is not None and ai_settings.saucer.dead:
        ai_settings.saucer = None

    # Update the enemy bullet chances.
    ai_settings.cur_frame_enemy_bullet += 0.5 * ai_settings.alien_speed_factor

    if ai_settings.cur_frame_enemy_bullet >= ai_settings.max_frame_enemy_bullet:
        random.seed(pygame.time.get_ticks())
        ai_settings.cur_frame_enemy_bullet = 0.0
        ai_settings.max_frame_enemy_bullet = 40 + random.randint(0, 40)
        num_aliens = len(aliens)

        if not num_aliens == 0:
            alien_index = random.randint(0, num_aliens-1)
            fire_bullet_enemy(ai_settings, screen, aliens.sprites()[alien_index], enemy_bullets)

    aliens.update()
    check_fleet_edges(ai_settings, aliens)

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ai_settings.ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets, barriers,
                 sprites, False)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets, barriers,
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
    if ai_settings.cur_frame_saucer >= 0.0:
        ai_settings.cur_frame_saucer += 0.5 * ai_settings.alien_speed_factor

    if ai_settings.cur_frame_saucer > ai_settings.max_frame_saucer:
        ai_settings.saucer = Saucer(ai_settings, screen, sprites)
        ai_settings.cur_frame_saucer = -1.0

        ai_settings.saucer.x = 0
        ai_settings.saucer.y = 128

    if ai_settings.saucer is not None:
        ai_settings.saucer.update()


def ship_hit(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets,
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
        end_level(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets, barriers, sprites)
    else:
        pygame.mixer.Sound.play(ai_settings.ship.sound_ship_destroyed)


def end_level(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets, barriers, sprites):
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    enemy_bullets.empty()
    barriers.empty()
    del ai_settings.saucer
    ai_settings.saucer = None
    ai_settings.cur_frame_saucer = 0
    ai_settings.cur_frame_ship_destroyed = 0.0
    ai_settings.ship_destroyed = False
    ai_settings.end_level = False

    pygame.mixer.music.stop()

    if stats.ships_left < 0:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        del ai_settings.ship
        ai_settings.current_sequence = 0
        sb.add_new_high_score(stats.score)
        stats.high_score = sb.high_scores[0]
        sb.export_new_high_scores()
        ai_settings.initialize_dynamic_settings()
        ai_settings.speedup_scale = 1.005
    else:
        # Create a new fleet and center the ship.
        ai_settings.initialize_dynamic_settings()
        create_fleet(ai_settings, screen, aliens, sprites)
        create_barriers(ai_settings, screen, barriers, sprites)
        ai_settings.ship.center_ship()


def check_aliens_bottom(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets,
                        barriers, sprites):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, aliens, bullets, enemy_bullets, barriers,
                     sprites, True)
            break


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
