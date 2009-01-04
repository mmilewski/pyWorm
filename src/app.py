#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet import clock, font, image, window
from pyglet.gl import *

from hud import HUD
from gameWorld import GameWorld
from camera import Camera
from inputManager import InputManager


class App(object):

    def __init__(self):
        fullscreen = False
        vsync = True
        
        if fullscreen:
            self.__window = window.Window( fullscreen=True, vsync=vsync )
        else:
            self.__window = window.Window( width=800, height=600, fullscreen=False, vsync=vsync )

        self.__winSize = winSize = ( self.__window.width, self.__window.height )

        self.__camera = Camera( winSize )
        self.__hud    = HUD( winSize )

        self.__inputManager = InputManager()
        self.__window.on_key_press   = self.__inputManager.key_pressed
        self.__window.on_key_release = self.__inputManager.key_released

        # clock.set_fps_limit(50) # FIXME: ??? usunąć to ???
        
        self.__world = GameWorld(self)        # to musi być na końcu

    def get_window_coords(self):
        ''' Zwraca współrzędne czworokąta, w którym można rysować. '''
        return self.__camera.windowCoords

    def register_input_observer(self, obj):
        self.__inputManager.register_observer(obj)

    def get_window_dim(self):
        ''' Zwraca wymiary okna (szerokość, wysokość) '''
        return (float(self.__window.width), float(self.__window.height))
        
    def main_loop(self):
        ''' Pętla główna gry. '''
        while not self.__window.has_exit:
            self.__window.dispatch_events()

            # update świata i HUDa
            dt = clock.tick()
#             if dt>0.001:
#                 print "FPS:", 1.0/dt
            self.__world.update( dt )
#             self.__hud.update( dt )

            # narysuj świat
            self.__camera.set3d()
            self.__world.draw()

            # narysuj HUD
#             self.__camera.set2d()
#             self.__hud.draw()

            self.__window.flip()
            
app = App()
app.main_loop()

