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
        self.print_y = 0
        self.print_x = 0
        self.changed_cursor_side = False
        self.page = 0
        self.page_max = 0
        self.page_list = []

    def draw(self):
        self.reset_cursor_position()
        self.game.screen.blit(self.image, (0, 0))
        self.page_max = len(self.game.datarecorder.devices) - 1

        # try:
        #     device_text = self.font.render(self.game.datarecorder.devices[list(self.game.datarecorder.devices.keys())[self.page]], False, self.text_color)
        #     device_rect = device_text.get_rect()
        #     self.game.screen.blit(device_text, (self.print_x, self.print_y))
        #     self.print_y += device_rect.height
        # except Exception as e:
        #     pass

        #
        # Device List contents
        # --------------------
        # Key: MAC address
        # 0: First Seen timestamp #datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M")
        # 1: Last Seen timestamp #datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M")
        # 2: Probe Count
        # 3: SSIDs requested - List
        # 4: Device Vendor
        # 5: Last signal strength
        # 6: Country Code
        # 7: MAC address


        #Print SSIDs broadcasted by device Probe Request
        try:
            device_list = self.game.datarecorder.devices[list(self.game.datarecorder.devices.keys())[self.page]]
            #Device Header
            self.draw_header('Device Details')
            self.draw_item('MAC: ' + device_list[7]) # 7: MAC address
            self.draw_item('Vendor: ' + device_list[4]) # 4: Device Vendor
            self.draw_item('Country Code: ' + device_list[6]) # 6: Country Code
            self.draw_item('First Seen: ' + device_list[0]) # 0: First Seen timestamp
            self.draw_item('Latest Seen: '+ device_list[1]) # 1: Last Seen
            self.draw_item('Latest Signal: ' + device_list[5]) # 5: Last signal strength
            self.draw_header('Probes')
            for item in device_list[3]:
                self.draw_item(item) # 3: SSIDs requested - List
            # for item in self.game.datarecorder.devices[list(self.game.datarecorder.devices.keys())[self.page]]:
            #     item_text = self.font.render(str(item), False, self.text_color)
            #     item_rect = item_text.get_rect()
            #     self.game.screen.blit(item_text, (self.print_x + 20, self.print_y))
            #     self.print_y += item_rect.height
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

    def draw_header(self, header):
        current_font_size = self.font_size
        self.change_fontsize(30)
        header_text = self.font.render(header, False, (255,140,0))
        header_rect = header_text.get_rect()
        self.game.screen.blit(header_text, (self.print_x, self.print_y))
        self.print_y += header_rect.height + 5
        self.change_fontsize(current_font_size)

    def draw_item(self, item):
        current_font_size = self.font_size
        item_text = self.font.render(item, False, self.text_color)
        item_rect = item_text.get_rect()
        self.game.screen.blit(item_text, (self.print_x, self.print_y))
        self.print_y += item_rect.height
        self.change_fontsize(current_font_size)

    def change_fontsize(self, newFontSize):
        self.font_size = newFontSize
        self.font = pg.font.SysFont('Consolas', self.font_size)

    def reset_cursor_position(self):
        self.print_y = 0
        self.print_x = 0
        self.changed_cursor_side = False

    def cursor_change_side(self):
        self.print_x = Width / 2
        self.print_y = 0
        self.changed_cursor_side = True
