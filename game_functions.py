import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien
import aliens_functions as af
import event_functions as ef
import collisions_functions as cf

# 监控按键事件
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
            bullets):
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            ef.check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            ef.check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            ef.check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                bullets, mouse_x, mouse_y)

# 更新屏幕
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

# 更新子弹
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    cf.check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
        aliens, bullets)

# 更新外星人
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    """
    af.check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        cf.ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    # 检查是否有外星人达到屏幕底端
    af.check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
