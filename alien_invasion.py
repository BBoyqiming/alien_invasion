# -*- coding:utf-8 -*-

import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion():
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""

        pygame.init()
        
        # 将 Setting 类传给 setting 属性，使其能访问 Setting 类中的配置信息
        self.settings = Settings()

        # 创建一个窗口，设置其尺寸，并赋给类属性
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # 此处的 self 表示将 AlienInvasion 实例传入 Ship 中，
        # 让 Ship 能够访问 AlienInvasion 类的资源，如 self.screen
        self.ship = Ship(self)

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 原先的监听事件功能、绘制屏幕功能均抽象为一个单独的方法，此处直接调用
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """监听键盘和鼠标事件"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # 向右移动飞船
                    self.ship.rect.x += 1
                elif event.key == pygame.K_LEFT:
                    self.ship.rect.x -= 1

    def _update_screen(self):
        """绘制屏幕"""

        # 方法被调用时重绘屏幕
        self.screen.fill(self.settings.bg_color)
            
        # 调用 Ship 类的 blitme 方法，每次被调用时绘制飞船
        self.ship.blitme()

        # 让最近绘制的屏幕可见，在 while 循环的作用下，屏幕会一直刷新
        pygame.display.flip()

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()

