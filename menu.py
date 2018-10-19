import pygame as pg
from settings import *
import os


class MenuBoard(pg.sprite.Sprite):

    def __init__(self, Game):
        self.game = Game
        self.groups = Game.all_sprites, Game.board
        self._layer = 1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((Width,Height))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centery = Height / 2
        self.rect.centerx = Width / 2


class MenuCursor(pg.sprite.Sprite):

    def __init__(self, Menu, Game):
        self.menu = Menu
        self.game = Game
        self.groups = Game.all_sprites, Game.cursor
        self._layer = 2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.menu.Board.rect.width,
                                self.menu.Items.rect.height))
        self.cursor_color = (0,0,255)
        self.image.fill(self.cursor_color)
        self.rect = self.image.get_rect()
        self.rect.y = self.menu.Items.menu_init_y + self.rect.height
        self.rect.centerx = Width / 2
        self.selectedItem = 0

    def down(self):
        if self.selectedItem < len(self.menu.Items.items[self.menu.Items.menu_section]) - 1:
            self.rect.y += self.rect.height
            self.selectedItem += 1

    def up(self):
        if self.selectedItem != 0:
            self.rect.y -= self.rect.height
            self.selectedItem -= 1

    def select(self):

#  MENU MAIN
        if self.menu.Items.menu_section == 'main':

            if self.selectedItem == 0:
                print('Live View')

            elif self.selectedItem == 1:
                self.game.reset_showing()
                self.game.showing_live_stats = True
                self.game.showing_menu = False
                print('Live Stats')

            elif self.selectedItem == 2:
                print('View All')

            elif self.selectedItem == 3:
                print('Map Devices')

            elif self.selectedItem == 4:
                print('Settings')
                self.menu.Items.menu_section = 'settings'
                self.reset_cursor_position()

#  MENU SETTINGS
        elif self.menu.Items.menu_section == 'settings':

            #  INVERT COLOR
            if self.selectedItem == 0:
                if self.menu.Items.text_color == (255,255,255):
                    self.menu.Items.text_color = (0,0,0)
                    self.menu.Board.image.fill((255,255,255))
                    self.cursor_color = (255,165,0)
                    self.image.fill(self.cursor_color)
                    self.game.livestats.image = self.game.livestats.images[1]
                else:
                    self.menu.Items.text_color = (255,255,255)
                    self.menu.Board.image.fill((0,0,0))
                    self.cursor_color = (0,0,255)
                    self.image.fill(self.cursor_color)
                    self.game.livestats.image = self.game.livestats.images[0]

            #  FONT SIZE
            elif self.selectedItem == 1:
                self.menu.Items.menu_section = 'font_size'
                self.reset_cursor_position()

            #  UPDATE
            elif self.selectedItem == 2:
                os.system('git pull')

            #  BACK
            elif self.selectedItem == 3:
                self.menu.Items.menu_section = 'main'
                self.reset_cursor_position()

#  MENU > SETTINGS > FONT SIZE
        elif self.menu.Items.menu_section == 'font_size':

            #  INCREASE
            if self.selectedItem == 0:
                self.menu.Items.update_font_size('increase')
                self.update_cursor_size(self.menu.Items.menu_init_y + (self.rect.height))

            #  DECREASE
            elif self.selectedItem == 1:
                self.menu.Items.update_font_size('decrease')
                self.update_cursor_size(self.menu.Items.menu_init_y + (self.rect.height*2))

            #  Reset
            elif self.selectedItem == 2:
                self.menu.Items.update_font_size('reset')
                self.update_cursor_size(self.menu.Items.menu_init_y + (self.rect.height*3))
                #  Is called twice, because it wont reset properly otherwise. Can't identify root cause
                self.update_cursor_size(self.menu.Items.menu_init_y + (self.rect.height*3))

            #  BACK
            elif self.selectedItem == 3:
                self.menu.Items.menu_section = 'settings'
                self.reset_cursor_position()


    def reset_cursor_position(self):
        self.rect.y = self.menu.Items.menu_init_y + self.rect.height
        self.selectedItem = 0

    def update_cursor_size(self, new_y):
        self.image = pg.Surface((self.menu.Board.rect.width,
                                self.menu.Items.rect.height))
        self.image.fill(self.cursor_color)
        self.rect = self.image.get_rect()
        self.rect.y = new_y
        self.rect.centerx = Width / 2


class MenuItems(pg.sprite.Sprite):

    def __init__(self, Menu, Game):
        self.menu = Menu
        self.game = Game
        self.groups = Game.all_sprites
        self._layer = 3
        pg.sprite.Sprite.__init__(self, self.groups)
        self.items = {}
        self.menu_section = 'main'
        self.font_size = 25
        self.text_color = (255,255,255)
        self.font = pg.font.SysFont('Consolas', self.font_size)
        self.image = self.font.render('', False, self.text_color)
        self.rect = self.image.get_rect()
        self.menu_init_y = 0
        self.text_size_y = self.rect.height

    def draw(self):
        counter = 0
        for item in self.items[self.menu_section]:
            counter += 1
            text_item = self.font.render(item, False, self.text_color)
            text_item_rect = text_item.get_rect()
            self.game.screen.blit(text_item, (self.menu.Cursor.rect.left * 1.2, self.menu_init_y + (text_item_rect.height * counter)))

    def update_font_size(self, action):
        if action == 'increase':
            self.font_size += 1
        elif action == 'decrease':
            self.font_size -= 1
        elif action == 'reset':
            self.font_size = 25
        self.font = pg.font.SysFont('Consolas', self.font_size)
        self.image = self.font.render('', False, self.text_color)
        self.rect = self.image.get_rect()


class Menu(MenuBoard, MenuCursor, MenuItems):

    def __init__(self, Game):
        self.Board = MenuBoard(Game)
        self.Items = MenuItems(self, Game)
        self.Cursor = MenuCursor(self, Game)
