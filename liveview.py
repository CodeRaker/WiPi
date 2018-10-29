import pygame as pg
import os
from settings import *

os.chdir('/root/wipi/')


class LiveView(pg.sprite.Sprite):
    """
    Displays a Live View of Collected data.
    """
    def __init__(self, Game):
        self.game = Game
        self.groups = Game.all_sprites
        self._layer = 1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = []
        self.images.append(pg.image.load('images/blank_blue_camo.bmp').convert())
        self.images.append(pg.image.load('images/blank_white_camo.bmp').convert())
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centery = Height / 2
        self.rect.centerx = Width / 2
        self.font_size = 21
        self.text_color = (255,255,255)
        self.font = pg.font.SysFont('Consolas', self.font_size)
        self.font_image = self.font.render('', False, self.text_color)
        self.rect = self.image.get_rect()
        self.print_y = 25
        self.print_x = 0
        self.changed_cursor_side = False
        self.page = 0
        self.page_max = 0
        self.page_list = []

    def draw(self):
        self.reset_cursor_position()
        self.game.screen.blit(self.image, (0, 0))
        self.page_max = len(self.game.datarecorder.devices) - 1

        try:
            device_text = self.font.render(self.game.datarecorder.devices[self.page], False, self.text_color)
            device_rect = device_text.get_rect()
            self.game.screen.blit(device_text, (self.print_x, self.print_y))
            self.print_y += device_rect.height
        except Exception as e:
            pass

        #Print SSIDs broadcasted by device Probe Request
        try:
            for item in self.game.datarecorder.devices[list(self.game.datarecorder.devices.keys())[self.page]]:
                item_text = self.font.render(str(item), False, self.text_color)
                item_rect = item_text.get_rect()
                self.game.screen.blit(item_text, (self.print_x + 20, self.print_y))
                self.print_y += item_rect.height
        except Exception as e:
            pass

        #Print Page Status
        try:
            page_status = str(self.page + 1) + '/' + str(self.page_max + 1)
            page_status_text = self.font.render(page_status, False, self.text_color)
            page_status_rect = page_status_text.get_rect()
            self.game.screen.blit(page_status_text, (Width - page_status_rect.width, Height - page_status_rect.height))
        except Exception as e:
            print(e)

        #Should print current page / total pages
        # #Print Devices
        # for device in self.game.datarecorder.devices:
        #     device_text = self.font.render(device, False, self.text_color)
        #     device_rect = device_text.get_rect()
        #     self.game.screen.blit(device_text, (self.print_x, self.print_y))
        #     self.print_y += device_rect.height
        #     if self.print_y > Height and not self.changed_cursor_side:
        #         self.cursor_change_side()
        #
        #     #Print SSIDs broadcasted by device Probe Request
        #     for probe in self.game.datarecorder.devices[device]:
        #         probe_text = self.font.render(probe, False, self.text_color)
        #         probe_rect = probe_text.get_rect()
        #         self.game.screen.blit(probe_text, (self.print_x + 20, self.print_y))
        #         self.print_y += probe_rect.height
        #         if self.print_y > Height and not self.changed_cursor_side:
        #             self.cursor_change_side()

    def reset_cursor_position(self):
        self.print_y = 0
        self.print_x = 0
        self.changed_cursor_side = False

    def cursor_change_side(self):
        self.print_x = Width / 2
        self.print_y = 0
        self.changed_cursor_side = True
