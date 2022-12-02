# -*- coding: utf-8 -*-

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""

        # 让外星人继承 Sprite 类
        super().__init__()
        # 让外星人得以访问游戏的其他资源，如 settings
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像，并设置外星人的 rect 属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近生成
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)
    
    def update(self):
        """让外星人向右或向右移动"""

        # 向特定方向移动特定距离，并更新 x 轴坐标
        # 方向由游戏引擎决定，根据游戏场景而变化
        # 移动速度由配置文件决定
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人触达了屏幕边缘，就返回 True"""

        # 获取游戏主屏幕矩形
        screen_rect = self.screen.get_rect()
        
        # 判断外星人右边缘是否超出屏幕右边缘，或者外星人的左边缘是否超出屏幕左边缘
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True