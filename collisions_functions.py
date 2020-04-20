from time import sleep

import pygame

from bullet import Bullet
from alien import Alien
import aliens_functions as af

# 检测精灵碰撞
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
        aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # 如果外星人全部被消灭，难度提升一个等级
    start_new_level(ai_settings, screen, stats, sb, ship, 
        aliens, bullets)


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应被外星人撞到飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        af.create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

# 其他检查
def check_high_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def start_new_level(ai_settings, screen, stats, sb, ship, 
        aliens, bullets):
    """提升游戏难度等级"""
    if len(aliens) == 0:
        # 如果整群外星人都被消灭，提高一个等级
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        af.create_fleet(ai_settings, screen, ship, aliens)