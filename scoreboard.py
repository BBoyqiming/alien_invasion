# -*- coding: utf-8 -*-

import pygame.font

class Scoreboard:
    """记分牌"""

    def __init__(self, ai_game):
        """初始化得分记录"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 记分牌的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 实例化记分牌图像
        self.prep_score()

    def prep_score(self):
        """将记分牌信息转化为图片"""

        rounded_score = round(self.stats.score, -1)
        score_str = '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, 
                                    self.text_color, self.settings.bg_color)

        # 将记分牌图像配置在屏幕右上方
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """将记分牌画出来"""

        self.screen.blit(self.score_image, self.score_rect)
