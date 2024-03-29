#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Moduł odpowiedzialny za rozruch programu.'''

from pyglet import clock, image, window
from pyglet.gl import *

from hud import HUD
from gameWorld import GameWorld
from camera import Camera
from inputManager import InputManager

import config
from splash import Splash        # splash screen

class App(object):

    def __init__(self):
        vsync = config.IS_VSYNC
        
        if config.IS_FULLSCREEN:
            self.__window = window.Window( fullscreen=True, vsync=vsync )
        else:
            width,height = config.WIN_SIZE
            self.__window = window.Window( width=width, height=height, fullscreen=False, vsync=vsync )

        self.__winSize = winSize = ( self.__window.width, self.__window.height )

        self.__camera = Camera( winSize )
        self.__hud    = HUD( winSize )

        self.__inputManager = InputManager()
        self.__window.on_key_press   = self.__inputManager.key_pressed
        self.__window.on_key_release = self.__inputManager.key_released

        if config.IS_FPS_LIMIT:
            clock.set_fps_limit( FPS_LIMIT )
        
        glDepthFunc( GL_LEQUAL )
        glEnable( GL_DEPTH_TEST )
        self.__world = GameWorld(self)        # to musi być na końcu

        
    def get_window_coords(self):
        ''' Zwraca współrzędne czworokąta, w którym można rysować. '''
        return self.__camera.windowCoords

    def register_input_observer(self, obj):
        self.__inputManager.register_observer(obj)

    def get_window_dim(self):
        ''' Zwraca wymiary okna (szerokość, wysokość) '''
        return (float(self.__window.width), float(self.__window.height))

    def get_window_draw_dim(self):
        ''' Zwraca współrzędne, w których należy rysować (szerokość, wysokość). '''
        return (1000.0, 750.0)
        # return (800.0, 600.0)    

    def main_loop(self):
        ''' Pętla główna gry. '''

        self.__timeElapsed = 0.0     # czas jaki upłynął od początku gry
        splash = Splash(self, self.__camera, config.SPLASH_DISPLAY_TIME)

        while not self.__window.has_exit:
            self.__window.dispatch_events()

            # update świata i HUDa
            dt = clock.tick() * config.DTIME_MULTIPLY
            self.__timeElapsed += dt

            if config.PRINT_FPS and dt>0.001:
                print "FPS:", 1.0/dt

            # ustaw kamerę
            self.__camera.set3d()

            # narysuj splash screen albo grę
            if self.__timeElapsed < config.SPLASH_DISPLAY_TIME:
                splash.update(dt)
                splash.draw()
            else:
                self.__world.update( dt )
#                 self.__hud.update( dt )

                # narysuj świat
                self.__camera.set3d()
                self.__world.draw()

#                 # narysuj HUD
#                 self.__camera.set2d()
#                 self.__hud.draw()

            self.__window.flip()
            
app = App()
app.main_loop()

