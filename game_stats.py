# -*- coding: utf-8 -*-

class GameStats:
    """统计游戏信息"""

    def __init__(self, ai_game):
        """初始化统计表"""

        self.settings = ai_game.settings
        self.reset_stats()

        # 启动游戏时，状态是 active
        self.game_active = True

    def reset_stats(self):
        """重置统计表"""
        self.ships_left = self.settings.ship_limit