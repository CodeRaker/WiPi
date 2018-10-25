import pygame as pg
import os
from settings import *
from menu import Menu
from colorpalette import *
from livestats import *
from liveview import *
from datarecorder import *
import RPi.GPIO as GPIO

os.chdir('/root/wipi/')

class Game:
    def __init__(self):
        os.environ["SDL_FBDEV"] = "/dev/fb1"
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((Width, Height))
        pg.display.set_caption('Menu')
        self.rgb = RGBColors()
        self.clock = pg.time.Clock()
        self.frameRate = frameRate
        self.frameCounter = 0
        self.running = True
        self.load_assets()
        self.showing_menu = False
        self.reset_menu = False
        self.showing_live_stats = False
        self.showing_live_view = False

    def load_assets(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.board = pg.sprite.Group()
        self.cursor = pg.sprite.Group()
        self.livestats = LiveStats(self)
        self.liveview = LiveView(self)
        self.datarecorder = DataRecorder(self)
        self.Menu = Menu(self)
        self.Menu.Items.items = {'main':['Live View','Statistics','View All','Map Devices','Settings'],'settings':['Invert Colors','Font Size','Update','Back'],'font_size':['Increase','Decrease','Reset','Back']}
        GPIO.setmode(GPIO.BCM)
        channel_list = [17, 22, 23, 27]
        GPIO.setup(channel_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.FALLING, callback=self.show_menu, bouncetime=200)
        GPIO.add_event_detect(22, GPIO.FALLING, callback=self.Menu.Cursor.up, bouncetime=200)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=self.Menu.Cursor.down, bouncetime=200)
        GPIO.add_event_detect(27, GPIO.FALLING, callback=self.Menu.Cursor.select, bouncetime=200)


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                os.system('killall python') #hard kill to handle multiprocesses, could be better, with a soft shutdown
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.Menu.Cursor.down()
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.Menu.Cursor.up()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.Menu.Cursor.select()
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.showing_menu = not self.showing_menu
                if self.showing_menu:
                    self.reset_menu = True

    def reset_showing(self):
        self.showing_live_stats = False
        self.showing_live_view = False

    def show_menu(self, channel):
        self.showing_menu = not self.showing_menu
        if self.showing_menu:
            self.reset_menu = True

    def update(self):
        self.all_sprites.update()
        self.datarecorder.update()

    def draw(self):
        self.screen.fill(self.rgb.black)
        #self.all_sprites.draw(self.screen)
        if self.showing_menu:
            if self.reset_menu:
                self.Menu.Items.menu_section == 'main'
                self.Menu.Cursor.reset_cursor_position()
                self.reset_menu = False
            self.board.draw(self.screen)
            self.cursor.draw(self.screen)
            self.Menu.Items.draw()
        elif self.showing_live_stats:
            self.livestats.draw()
        elif self.showing_live_view:
            self.liveview.draw()


    def run(self):
        while self.running:
            self.frameCounter += 1
            self.clock.tick(self.frameRate)
            self.events()
            self.update()
            self.draw()
            pg.display.flip()
            if self.frameCounter == self.frameRate:
                self.frameCounter = 0

g = Game()
while g.running:
    g.run()
pg.quit()
