# -*- coding:utf-8 -*-

import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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
            self.ship.update()
            self._update_bullets()
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

    # part4: 管理外星人

    def _create_fleet(self):
        """创建外星人舰队"""

        # 创建一个外星人实例并加入外星人编组
        alien = Alien(self)
        self.aliens.add(alien)


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


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()

