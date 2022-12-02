# -*- coding: utf-8 -*-

class Settings:
    """
    存储游戏 Alien Invasion 中所有设置的类
    相当于游戏的配置文件
    """

    def __init__(self):
        """初始化游戏的设置"""

        # 屏幕设置：尺寸和颜色
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置：飞船速度和飞船生命值
        self.ship_speed = 1.5
        self.ship_limit = 3

        # 子弹设置：尺寸、速度、颜色、最大数量
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # 外星人设置：横向移动速度、下降速度、默认横向移动方向
        self.alien_speed = 1
        self.fleet_drop_speed = 100
        # 1 代表舰队想右移动，-1 代表向左
        # 会通过类方法来控制舰队方向的变化
        self.fleet_direction = 1