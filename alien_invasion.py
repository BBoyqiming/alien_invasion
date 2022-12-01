# -*- coding: utf-8 -*-

import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats


# 此为游戏主程序，主要功能包括：
# - 启动游戏
# - 监听并响应玩家操作（键盘操作）
# - 持续刷新屏幕，实现响应内容的更新


class AlienInvasion():
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""

        pygame.init()
        
        # 将 Setting 实例化并传给 setting 属性，使后者能访问 Setting 类中存储的配置信息
        self.settings = Settings()

        # 创建一个窗口对象，设置其尺寸，并赋给 screen 属性
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        # 全屏游戏方法
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # 创建一个统计表
        self.stats = GameStats(self)

        # 此处的 self 表示将 AlienInvasion 传入 Ship 中
        # 让 Ship 能够访问 AlienInvasion 类的属性、方法
        # 这是为什么 Ship 有参数 ai_game 的原因
        # Bullet 同理
        self.ship = Ship(self)
        
        # 创建一个存储子弹的编组
        self.bullets = pygame.sprite.Group()

        # 创建一个外星人的编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    # part1: 游戏主循环

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 原先的监听事件功能、绘制屏幕功能均抽象为一个单独的方法，此处直接调用
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    # part2: 按键监听与响应

    def _check_events(self):
        """监听键盘和鼠标事件"""

        for event in pygame.event.get():
            # 点击右上角关闭退出游戏
            if event.type == pygame.QUIT:
                sys.exit()
            # 监听按下按键
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # 监听松开按键
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键"""

        # 按右键，变更 Ship 属性值，使其开始右移
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # 按左键，变更 Ship 属性值，使其开始左移
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""

        # 松右键，变更 Ship 属性值，使其停止右移
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        # 松左键，变更 Ship 属性值，使其停止左移
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # part3: 子弹处理

    def _fire_bullet(self):
        """
        按下空格键时触发此方法
        如果此时子弹数量小于最大数量，创建一颗子弹，并将其加入编组 bullets 中
        否则无行动
        """

        # Setting 类中限制了子弹的最大数量
        if len(self.bullets) < self.settings.bullets_allowed:
            # 向 Bullet 类中传入 AlienInvasion 类，使前者可以访问后者的属性和方法
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """对子弹进行刷新，并删除消失的子弹"""

        # 更新子弹的位置
        self.bullets.update()

        # 检查每个子弹是否飞出屏幕外，如是则删除
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """处理子弹和外星人的撞击"""
        # 检查每个子弹是否集中外星人，如是则消除子弹和外星人
        collisions = pygame.sprite.groupcollide(
                    self.bullets, self.aliens, True, True)

        if not self.aliens:
            # 当最后一个外星人被摧毁，就清空子弹并创建新的舰队
            self.bullets.empty()
            self._create_fleet()

    # part4: 管理外星人

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其放置某一行的某个位置"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        # alien.rect.x = alien_width + 2 * alien_width * alien_number
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """创建外星人舰队"""
        
        # 两个外星人之间的距离等于一个外星人的宽度
        # 创建一个外星人实例，仅用于提取外星人宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # 计算屏幕中一行能放几个外星人，先减去两边的 margin
        avaliable_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = avaliable_space_x // (2 * alien_width)

        # 计算大概能放几行外星人（要预留一些Y轴空间作为飞船空间）
        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)
        number_rows = avaliable_space_y // (2 * alien_height)

        # 通过计算得出的一行数量，创建多个外星人实例并加入外星人编组
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """
        判断舰队内是否有任何一个外星人碰到屏幕边缘
        如果有的话，就调用让整个舰队下移的方法
        """

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """调用该方法时，让整个舰队往下移动"""
        
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """
        1. 判断舰队是否触达屏幕边缘
        2. 更新舰队所有外星人的位置
        """

        self._check_fleet_edges()
        # 用 aliens 而不是 alien
        # 是因为要通过群组对象，一次性调用其中所有外星人实例的 update 方法
        self.aliens.update()

        # 判断外星人是否和飞船相撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print('Ship hit!!!')
            self._ship_hit()

        # 检查外星人是否触达屏幕底部
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检查外星人是否触达屏幕底部"""

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    # part5: 屏幕绘制

    def _update_screen(self):
        """绘制屏幕"""

        # 方法被调用时重绘屏幕
        self.screen.fill(self.settings.bg_color)
            
        # 调用 Ship 类的 blitme 方法，绘制飞船
        self.ship.blitme()

        # 调用 Bullet 的 draw_bullet 方法，对还在编组中的每个子弹进行绘制
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        # 调用 pygame 编组的自带方法来绘制外星人
        self.aliens.draw(self.screen)

        # 让最近绘制的屏幕可见，在 while 循环的作用下，屏幕会一直刷新
        pygame.display.flip()

    # part6: 飞船生命值

    def _ship_hit(self):
        """响应飞船撞毁事件"""

        if self.stats.ships_left > 0:
            # 减少飞船生命值
            self.stats.ships_left -= 1

            # 撞毁时，清空所有外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 清空后，创建新的外星人舰队
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)

        else:
            self.stats.game_active = False


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()

