import pygame as pg
from settings import *


class MenuBoard(pg.sprite.Sprite):

    def __init__(self, Game):
        self.game = Game
        self.groups = Game.all_sprites
        self._layer = 1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((Width*0.9,Height*0.9))
        self.image.fill((0,255,255))
        self.rect = self.image.get_rect()
        self.rect.centery = Height / 2
        self.rect.centerx = Width / 2


class MenuCursor(pg.sprite.Sprite):

    def __init__(self, Menu, Game):
        self.menu = Menu
        self.game = Game
        self.groups = Game.all_sprites
        self._layer = 2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.menu.Board.rect.width * 0.97,
                                self.menu.Items.rect.height))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.y = self.menu.Items.menu_init_y + self.rect.height
        self.rect.centerx = Width / 2
        self.selectedItem = 0

    def down(self):
        if self.selectedItem < len(self.menu.Items.items) - 1:
            self.rect.y += self.rect.height
            self.selectedItem += 1

    def up(self):
        if self.selectedItem != 0:
            self.rect.y -= self.rect.height
            self.selectedItem -= 1

    def select(self):
        print(str(self.selectedItem))


class MenuItems(pg.sprite.Sprite):

    def __init__(self, Menu, Game):
        self.menu = Menu
        self.game = Game
        self.groups = Game.all_sprites
        self._layer = 3
        pg.sprite.Sprite.__init__(self, self.groups)
        self.items = []
        self.font = pg.font.SysFont('Consolas', 30)
        self.image = self.font.render('', False, (255,255,255))
        self.rect = self.image.get_rect()
        self.menu_init_y = 10
        self.text_size_y = self.rect.height

    def draw(self):
        counter = 0
        for item in self.items:
            counter += 1
            text_item = self.font.render(item, False, (255,255,255))
            text_item_rect = text_item.get_rect()
            self.game.screen.blit(text_item, (self.menu.Cursor.rect.left * 1.2, self.menu_init_y + (text_item_rect.height * counter)))


class Menu(MenuBoard, MenuCursor, MenuItems):

    def __init__(self, Game):
        self.Board = MenuBoard(Game)
        self.Items = MenuItems(self, Game)
        self.Cursor = MenuCursor(self, Game)
