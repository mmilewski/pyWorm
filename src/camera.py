#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet.gl import *

class Camera(object):

    def __init__(self, winSize):

        # (szerokość, wysokość)
        self.__winSize = winSize
        ratio = float(self.__winSize[1]) / self.__winSize[0]

        # +------------(1,ratio)
        # |                    |
        # (0,0)----------------+
        self.__windowCoords = (0, 1, 0, ratio)   # xmin,xmax,ymin,ymax

        # płaszczyzny obcinania
        self.__znearFar = (-1, 100)

    windowCoords = property(lambda self: self.__windowCoords)


    def set3d(self):
        ''' Ustawia projekcję na trójwymiarową. '''
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho( *self.__windowCoords + self.__znearFar )


    def set2d(self):
        ''' Ustawia projektcję na dwuwymiarową. '''
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D( 0, self.__winSize[0], 0, self.__winSize[1])


    def look_at(self, pos, center, up):
        ''' Ustawia kamerę w pozycji pos, kieruje ją w punkt center.
        Up oznacza wektor 'w górę'. '''
        if not len(pos+center+up)==9:
            print "Error: do look_at wymagane są 3 krotki po 3 współrzędne"
        else:
            gluLookAt( *(pos+center+up) )
