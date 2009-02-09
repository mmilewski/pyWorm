#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Moduł odpowiada za wyświetlenie animowanego ekranu z nazwą gry.'''

from pyglet.gl import *
from pyglet import image
from os.path import join

class Splash(object):
    ''' Klasa obsługująca obrazek na wejście.'''

    def __init__(self, app, camera, showTime):
        self.__theApp = app
        self.__camera = camera
        splashImage = image.load( join('..','gfx','splash.png') )
        self.__texture = splashImage.texture
        self.__alpha = 0.0
        self.__showTime = showTime

    def draw(self):
        ''' Rysuje.'''
        glClearColor( 0, 0, 0, 0.5 )
        glClear( GL_COLOR_BUFFER_BIT )
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

        glTranslatef( 0, 0, -1 )
        x,w,y,h = self.__camera.windowCoords
        glScalef( w, h, 1 )

        glColor4f( 1, 1, 1, self.__alpha )
        glEnable( GL_TEXTURE_2D )
        assert glIsTexture( self.__texture.id )
        glBindTexture( GL_TEXTURE_2D, self.__texture.id )

        tc = [ (0,0), (1,0), (1,1), (0,1) ]
        vs = [ (0,0,0), (1,0,0), (1,1,0), (0,1,0) ]
        glBegin( GL_QUADS )
        for v,t in zip(vs,tc):
            glTexCoord2f( *t )
            glVertex3f( *v )
        glEnd()

        glFlush()

    def update(self,dt):
        ''' Aktualizuje animację.'''
        self.__alpha+=dt/self.__showTime
