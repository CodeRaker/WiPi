import pygame as pg
from settings import *

class LiveStats(pg.sprite.Sprite):
    """
    Displays Live Statistics from the unit. CPU, RAM, Packets/Sec
    """
    def __init__(self, Game):
        self.game = Game
        self.groups = Game.all_sprites, Game.livestats_group
        self._layer = 1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = []
        self.images.append(pg.image.load('images/livestats_black.png').convert())
        self.images.append(pg.image.load('images/livestats_white.png').convert())
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centery = Height / 2
        self.rect.centerx = Width / 2
