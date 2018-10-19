import pygame as pg
from settings import *

class LiveStats(pg.sprite.Sprite):
    """
    Displays Live Statistics from the unit. CPU, RAM, Packets/Sec
    """
    def __init__(self, Game):
        self.game = Game
        self.groups = Game.all_sprites#, Game.livestats_group
        self._layer = 1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = []
        self.images.append(pg.image.load('images/livestats_black.png').convert())
        self.images.append(pg.image.load('images/livestats_white.png').convert())
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centery = Height / 2
        self.rect.centerx = Width / 2
        self.font_size = 20
        self.text_color = (255,255,255)
        self.font = pg.font.SysFont('Consolas', self.font_size)
        self.font_image = self.font.render('', False, self.text_color)
        self.rect = self.image.get_rect()

    def draw(self):
        self.game.screen.blit(self.image, (0, 0))

        #Total Packets
        self.update_font_size(20)
        total_packets_text = self.font.render(str(self.game.datarecorder.total_packets), False, self.text_color)
        total_packets_rect = total_packets_text.get_rect()
        self.game.screen.blit(total_packets_text, (total_packets_rect.left + 90, 23))

        #Total Packets per Second
        self.update_font_size(120)
        total_packets_per_second_text = self.font.render(str(self.game.datarecorder.total_packets_per_second), False, self.text_color)
        total_packets_per_second_rect = total_packets_per_second_text.get_rect()
        self.game.screen.blit(total_packets_per_second_text, (total_packets_per_second_rect.left + 195, 23))

    def update_font_size(self, FontSize):
        self.font = pg.font.SysFont('Consolas', FontSize)
