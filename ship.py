# -*- coding:utf-8 -*-

import pygame

class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        
        # 使 Ship 类也能访问 Settings 类中的配置
        self.settings = ai_game.settings

        # ai_game 的参数名含义是此处用于传入 AlienInvasion 类
        # 将 AlienInvasion 类的 screen 属性赋给了 Ship 类的 screen 属性
        # 即让 Ship 的 screen 属性指向了 pygame 绘制出的屏幕对象
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都将其放置在屏幕底部的中央
        # 让飞船外接矩形底部中间的位置等于屏幕底部中间的位置
        self.rect.midbottom = self.screen_rect.midbottom

        # rect 的 x 属性不支持小数，此处将其转化为小数
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标准调整飞船的位置"""

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 根据 self.x 更新 rect 对象
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""

        self.screen.blit(self.image, self.rect)