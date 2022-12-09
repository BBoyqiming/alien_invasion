# -*- coding: utf-8 -*-

class Settings:
    """
    存储游戏 Alien Invasion 中所有设置的类
    相当于游戏的配置文件
    """

    def __init__(self):
        """初始化游戏的固定配置"""

        # 屏幕设置：尺寸和颜色
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船生命值设置
        self.ship_limit = 3

        # 子弹设置：尺寸、颜色、最大数量
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # 外星人下降速度设置
        self.fleet_drop_speed = 10

        # 游戏加速倍率设置
        self.speedup_scale = 1.3

        # 得分倍率设置
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化会随游戏进程而变化的配置"""

        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.5

        # 1 代表外星人舰队想右移动，-1 代表向左
        # 会通过方法来控制舰队方向的变化
        self.fleet_direction = 1

        # 击落一个外星人的分数
        self.alien_points = 10

    def increase_speed(self):
        """使游戏加速"""

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= int(self.alien_points * self.score_scale)