#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet.gl import *
import os.path
from pyglet import image
from render_toolkit import draw_textured_quad, compute_tex_vertex_coords


class BackgroundManager(object):

    def __init__( self, levelManager ):
        self.__backgroundTexture = None                 # tekstura tła
        self.__backgroundOffset = 0                     # zamiast obiektów przesuwamy tło
        self.__window_coords = None                     # wymiar okna (np. 800x600)
        self.__window_draw_dim = None                   # przeskalowany wymiar okna (np. 1,0.75)
        self.__levelManager = levelManager

    def set_window_coords(self, coords):
        self.__window_coords = coords

    def set_window_draw_dim(self, dim):
        self.__window_draw_dim = dim


    def update( self, dt ):
        ''' Aktualizuje tło'''

        # aktualizacja przesuwania tła
        self.__backgroundOffset+= dt/35


    def draw_background( self ):
        ''' Rysuje tło poziomu.'''

        # przelicz współrzędne tekstury i czworokąta z tłem
        coords = self.__window_coords   # czworokąt zajmujący cały ekran
        x0,x1,y0,y1 = coords[0], coords[1], coords[2], coords[3]
        off = self.__backgroundOffset       # przesunięcie tła (mapa stoi,poruszamy tłem)
        tc = [ ( 0+off,  0), ( .5+off,  0), ( .5+off,  1), ( 0+off,  1) ]
        vs = [ ( x0, y0), ( x1, y0), ( x1, y1), ( x0, y1) ]

        # jeżeli to konieczne to wczytaj teksturę z tłem
        if not self.__backgroundTexture:
            bgfilename = self.__levelManager.get_background_filenames()[0]
            spriteImagePath = os.path.join( "..", "gfx", bgfilename )
            img = image.load( spriteImagePath )
            self.__backgroundTexture = img.get_texture()

        # narysuj czworokąt z tłem
        if self.__backgroundTexture:
            textureId = self.__backgroundTexture.id
            draw_textured_quad( tc, vs, textureId )

