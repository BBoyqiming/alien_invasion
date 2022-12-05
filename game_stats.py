# -*- coding: utf-8 -*-

class GameStats:
    """游戏数据统计"""

    def __init__(self, ai_game):
        """初始化游戏数据"""

        # 让 GameStats 类能访问游戏的资源，如 settings
        self.settings = ai_game.settings
        
        # 每次初始化时，调用方法清空统计表
        self.reset_stats()

        # 启动游戏时，游戏状态是 False，游戏不运行
        # 游戏中通过主引擎更改状态为 True，此时游戏运行
        self.game_active = False

    def reset_stats(self):
        """重置飞船生命值"""

        # 将飞船剩余生命值重置为配置中的飞船生命值
        self.ships_left = self.settings.ship_limit