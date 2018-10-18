import pygame as pg
from settings import *
from menu import Menu
from colorpalette import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((Width, Height))
        pg.display.set_caption('Menu')
        self.rgb = RGBColors()
        self.clock = pg.time.Clock()
        self.frameRate = frameRate
        self.frameCounter = 0
        self.running = True
        self.loadAssets()

    def loadAssets(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.Menu = Menu(self)
        self.Menu.Items.items = ['item1','item2','item3','VeryNiceMenu!']

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.Menu.Cursor.down()
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.Menu.Cursor.up()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.Menu.Cursor.select()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(self.rgb.black)
        self.all_sprites.draw(self.screen)
        self.Menu.Items.draw()

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
