# -*- coding: utf-8 -*-

import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button


# 此为游戏主程序，主要功能包括：
# - 启动游戏
# - 监听并响应玩家操作（键盘操作）
# - 持续刷新屏幕，实现响应内容的更新


class AlienInvasion():
    """
    管理游戏资源和行为的类
    即：游戏引擎
    """

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

        # 创建一个数据统计对象
        self.stats = GameStats(self)

        # 此处的 self 表示将 AlienInvasion 传入 Ship 中
        # 让 Ship 能够访问 AlienInvasion 类的属性、方法
        # 这是为什么 Ship 有参数 ai_game 的原因
        # Bullet 同理
        self.ship = Ship(self)
        
        # 创建一个子弹编组
        self.bullets = pygame.sprite.Group()

        # 创建一个外星人编组，并创建舰队
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # 创建开始按钮
        self.play_button = Button(self, 'Play!')

    # part1: 游戏主循环

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 原先的监听事件功能、绘制屏幕功能均抽象为一个单独的方法，此处直接调用
            self._check_events()

            # 判断游戏是否处于激活状态，如果是，则运行核心功能
            # 若否，则飞船、子弹、外星人均停止活动
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            # 最后才更新屏幕
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键"""

        # 按右键，变更 Ship 属性值，使其开始右移
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # 按左键，变更 Ship 属性值，使其开始左移
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # 按 Q 键退出游戏
        elif event.key == pygame.K_q:
            sys.exit()
        # 按空格键发射子弹
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

    def _check_play_button(self, mouse_pos):
        """单击开始按钮时启动游戏"""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # 游戏处于激活状态时，点击按钮所在区域不会有反应
        if button_clicked and not self.stats.game_active:

            # 重置游戏配置
            self.settings.initialize_dynamic_settings()

            # 隐藏鼠标
            pygame.mouse.set_visible(False)

            # 重置数据统计信息
            self.stats.reset_stats()
            self.stats.game_active = True

            # 清空外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建新的外星人，并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

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
            # 将子弹加入编组
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """对子弹进行刷新，并删除消失的子弹"""

        # 更新子弹的位置
        self.bullets.update()

        # 检查每个子弹是否飞出屏幕外，如是则删除
        # 为什么要使用 copy 方法？
        # 本方法有可能删除掉编组中的一个成员
        # 所以不能直接对原编组进行遍历，因为有可能导致遍历过程中编组成员发生变化
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        # 判断和处理子弹与外星人的撞击
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """处理子弹和外星人的撞击"""

        # 检查是否有任一子弹击中外星人，如是则消除子弹和外星人
        collisions = pygame.sprite.groupcollide(
                    self.bullets, self.aliens, True, True)

        # 理论上这个判断可以放在外部，放在这里出于逻辑顺畅：相撞 --> 判断是否清空
        if not self.aliens:
            # 当最后一个外星人被摧毁，就清空子弹并创建新的舰队，并使游戏加速
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    # part4: 管理外星人

    def _create_fleet(self):
        """创建外星人舰队"""
        
        # 创建一个外星人实例，仅用于提取外星人宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # 计算屏幕中一行能放几个外星人，先减去两边的 margin
        avaliable_space_x = self.settings.screen_width - (2 * alien_width)
        # 两个外星人之间的距离等于一个外星人的宽度
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

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其放置某一行的某个位置"""

        # 创建一个外星人实例，设置其尺寸、位置，并加入编组
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        # alien.rect.x = alien_width + 2 * alien_width * alien_number
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """
        1. 判断舰队是否触达屏幕边缘，并做相应处理
        2. 更新舰队所有外星人的位置，更新处理结果
        """

        self._check_fleet_edges()
        # 用 aliens 而不是 alien
        # 是因为要通过群组对象，一次性调用其中所有外星人实例的 update 方法
        self.aliens.update()

        # 判断外星人是否和飞船相撞，如果是则扣除飞船生命值
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print('Ship hit!!!')
            self._ship_hit()

        # 检查外星人是否触达屏幕底部
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """
        判断舰队内是否有任一外星人碰到屏幕边缘
        如果有，就调用方法以变更舰队移动方向
        """

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """调用该方法时，改变舰队横向移动方向，并让舰队整体向下移动"""
        
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """检查外星人是否触达屏幕底部，如果是则扣除飞船生命值"""

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    # part5: 飞船生命值

    def _ship_hit(self):
        """响应飞船撞毁事件"""

        # 若飞船生命值未归零
        if self.stats.ships_left > 0:
            # 减少飞船生命值
            self.stats.ships_left -= 1

            # 撞毁时，清空所有外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 清空后，创建新的外星人舰队
            self._create_fleet()
            # 飞船对象并未消失，通过使其居中的方式，模拟出“复活”的效果
            self.ship.center_ship()

            # 暂停一会
            sleep(0.5)

        # 若飞船生命值未归零，更改游戏激活状态
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    # part6: 屏幕绘制

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

        # 在游戏未激活时，将按钮绘制在屏幕上
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见，在 while 循环的作用下，屏幕会一直刷新
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()

