# -*- coding: utf-8 -*-

import pygame.font

class Button:
    """管理按钮的类"""

    def __init__(self, ai_game, msg):
        """初始化界面上的按钮"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建一个按钮并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 设置按钮信息
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将信息转化为一个图像并放置在按钮中央"""

        self.msg_image = self.font.render(msg, True, self.text_color, 
                        self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制按钮"""

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)