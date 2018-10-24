import pygame as pg
import psutil
import math
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
        self.images.append(pg.image.load('images/livestats_blue_camo.png'))#.convert())
        self.images.append(pg.image.load('images/livestats_white.png'))#.convert())
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centery = Height / 2
        self.rect.centerx = Width / 2
        self.font_size = 21

        self.text_color = (255,255,255)
        self.font = pg.font.SysFont('Consolas', self.font_size)
        self.font_image = self.font.render('', False, self.text_color)
        self.rect = self.image.get_rect()

        #CPU INIT
        self.cpu_text = self.font.render(str(psutil.cpu_percent()), False, self.text_color)
        self.cpu_rect = self.cpu_text.get_rect()
        self.cpu_bar = pg.Surface((100,20))
        self.cpu_bar.fill((0,255,255))
        self.cpu_bar_rect = self.cpu_bar.get_rect()
        self.cpu_bar_rect.y = 161
        self.cpu_bar_rect.right = Width*2

        self.mem_text = self.font.render(str(psutil.virtual_memory()[2]), False, self.text_color)
        self.mem_rect = self.mem_text.get_rect()
        self.mem_bar = pg.Surface((100,20))
        self.mem_bar.fill((0,255,255))
        self.mem_bar_rect = self.cpu_bar.get_rect()
        self.mem_bar_rect.y = 181
        self.mem_bar_rect.right = Width*2

        self.disk_text = self.font.render(str(psutil.disk_usage('/')[3]), False, self.text_color)
        self.disk_rect = self.disk_text.get_rect()
        self.disk_bar = pg.Surface((100,20))
        self.disk_bar.fill((0,255,255))
        self.disk_bar_rect = self.cpu_bar.get_rect()
        self.disk_bar_rect.y = 201
        self.disk_bar_rect.right = Width*2


    def draw(self):
        self.game.screen.blit(self.image, (0, 0))

        #Total Packets
        self.update_font_size(21)
        total_packets_text = self.font.render(str(self.game.datarecorder.total_packets), False, self.text_color)
        total_packets_rect = total_packets_text.get_rect()
        total_packets_rect.right = 120
        total_packets_rect.y = 24
        self.game.screen.blit(total_packets_text, total_packets_rect)

        #Total Packets per Second
        self.update_font_size(140)
        total_packets_per_second_text = self.font.render(str(self.game.datarecorder.total_packets_per_second), False, self.text_color)
        total_packets_per_second_rect = total_packets_per_second_text.get_rect()
        total_packets_per_second_rect.right = Width - 35
        total_packets_per_second_rect.y = 26
        self.game.screen.blit(total_packets_per_second_text, total_packets_per_second_rect)

        #Total Beacons
        self.update_font_size(21)
        total_beacons_text = self.font.render(str(self.game.datarecorder.total_beacons), False, self.text_color)
        total_beacons_rect = total_beacons_text.get_rect()
        total_beacons_rect.right = 120
        total_beacons_rect.y = 62
        self.game.screen.blit(total_beacons_text, total_beacons_rect)

        #Total Beacons per Second
        self.update_font_size(90)
        total_beacons_per_second_text = self.font.render(str(self.game.datarecorder.total_beacons_per_second), False, self.text_color)
        total_beacons_per_second_rect = total_beacons_per_second_text.get_rect()
        total_beacons_per_second_rect.x = 30
        total_beacons_per_second_rect.y = 150
        self.game.screen.blit(total_beacons_per_second_text, total_beacons_per_second_rect)

        #Total Probes
        self.update_font_size(21)
        total_probes_text = self.font.render(str(self.game.datarecorder.total_probes), False, self.text_color)
        total_probes_rect = total_probes_text.get_rect()
        total_probes_rect.right = 120
        total_probes_rect.y = 44
        self.game.screen.blit(total_probes_text, total_probes_rect)

        #Collects stats once per second, otherwise it fucks up
        if self.game.frameCounter == 1:

            #CPU Number
            self.update_font_size(21)
            cpu_usage = psutil.cpu_percent()
            self.cpu_text = self.font.render(str(cpu_usage), False, self.text_color)
            self.cpu_rect = self.cpu_text.get_rect()

            #CPU Bar
            self.cpu_bar = pg.Surface((100,20))
            self.cpu_bar.fill((128,0,0))
            self.cpu_bar = pg.transform.scale(self.cpu_bar, (int(str(math.ceil(cpu_usage)*0.7).split('.')[0]), 13))
            self.cpu_bar_rect = self.cpu_bar.get_rect()
            self.cpu_bar_rect.y = 160
            self.cpu_bar_rect.right = Width - 40

            #Memory
            mem_usage = psutil.virtual_memory()[2]
            self.mem_text = self.font.render(str(mem_usage), False, self.text_color)
            self.mem_rect = self.mem_text.get_rect()

            #Memory Bar
            self.mem_bar = pg.Surface((100,20))
            self.mem_bar.fill((0,128,0))
            self.mem_bar = pg.transform.scale(self.mem_bar, (int(str(math.ceil(mem_usage)*0.7).split('.')[0]), 13))
            self.mem_bar_rect = self.mem_bar.get_rect()
            self.mem_bar_rect.y = 180
            self.mem_bar_rect.right = Width - 40

            #DISK
            disk_usage = psutil.disk_usage('/')[3]
            self.disk_text = self.font.render(str(disk_usage), False, self.text_color)
            self.disk_rect = self.disk_text.get_rect()

            #DISK Bar
            self.disk_bar = pg.Surface((100,20))
            self.disk_bar.fill((0,0,128))
            self.disk_bar = pg.transform.scale(self.disk_bar, (int(str(math.ceil(disk_usage)*0.7).split('.')[0]), 13))
            self.disk_bar_rect = self.disk_bar.get_rect()
            self.disk_bar_rect.y = 200
            self.disk_bar_rect.right = Width - 40

        self.game.screen.blit(self.cpu_bar, self.cpu_bar_rect)
        self.game.screen.blit(self.mem_bar, self.mem_bar_rect)
        self.game.screen.blit(self.disk_bar, self.disk_bar_rect)
        self.game.screen.blit(self.cpu_text, (self.cpu_rect.left + 290, 163))
        self.game.screen.blit(self.mem_text, (self.mem_rect.left + 290, 183))
        self.game.screen.blit(self.disk_text, (self.disk_rect.left + 290, 203))



    def update_font_size(self, FontSize):
        self.font = pg.font.SysFont('Consolas', FontSize)
