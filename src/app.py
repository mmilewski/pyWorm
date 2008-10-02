#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet import clock, font, image, window
from pyglet.gl import *

from collisionManager import CollisionManager
from spriteManager import SpriteManager, SpriteFrame
from gameObject import Triangle
from gameWorld import GameWorld
from camera import Camera
from spriteStrategy import SpriteScriptStrategy
from spriteScript import SpriteScript

class App(object):

    def __init__(self):
        self.__world = GameWorld()
        fullscreen = False
        vsync = True
        
        if fullscreen:
            self.win = window.Window( fullscreen=True, vsync=vsync )
        else:
            self.win = window.Window( width=800, height=600, fullscreen=False, vsync=vsync )

        winSize = ( self.win.width, self.win.height )
        print "Utworzono okno o rozmiarze:", winSize, "Fullscreen:", fullscreen
        self.camera = Camera( winSize )
        print "Wymiary w 3d: ", self.camera.windowCoords, "(lewy, szerokość, dół, wysokość)"
#         self.hud = Hud( winSize )
#         clock.set_fps_limit(50)

        # dodaj obiekty do świata
        self.add_objects()

    world = property( lambda self:self.__world )


    def __add_scripted_object( self, spriteName, object ):
        scriptFilename = spriteName + '.sprite'
        object.spriteName = spriteName
        # załaduj skrypt
        script = SpriteScript()
        script.load_from_file( scriptFilename, resourceDir='../gfx' )
        # dodaj strategię na podstawie skryptu
        object.spriteStrategy = SpriteScriptStrategy( script )

        #
        # FIXME
        # rozdzielenie skryptu na skrypt do zmiany stanu animacji i skrypt do
        # wyświetlania animacji
        #

        # dodaj skrypt do menadżera skryptów
        self.world.spriteManager.add_script( object.spriteName, script )
        # dodaj obiekt do świata
        self.world.add_object( object )


    def add_objects(self):
        self.__add_scripted_object( 'bang', Triangle() )

    def main_loop(self):
        ''' Pętla główna gry. '''
        while not self.win.has_exit:
            self.win.dispatch_events()

            # update świata i HUDa
            dt = clock.tick()
            self.world.update( dt )
#             self.hud.update( dt )

            # narysuj świat
            self.camera.set3d()
            self.world.draw()

            # narysuj HUD
            self.camera.set2d()
#             self.hud.draw()

            self.win.flip()

app = App()
app.main_loop()

