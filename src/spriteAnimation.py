#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet import resource, image


class SpriteAnimation(object):
    def __init__(self, animDict, imageFilename):
        self.__imageFilename = imageFilename

        try:
            self.__texture = image.load( imageFilename ).get_texture() if imageFilename else None
        except :
            print "Error: ładowanie tekstury z pliku nie powiodło się (%s)." % imageFilename
        try:
            anim = animDict
            self.__yoff = (anim['yoff'] if anim.has_key('yoff') else 0)  # default
            self.__xoff = (anim['xoff'] if anim.has_key('xoff') else 0)  # default
            self.__frameCount = anim['frames_count']
            self.__duration = anim['duration'] / self.__frameCount / 1000.0
            self.__wid, self.__hei = anim['frame']
            self.__colCount = anim['cols']
        except KeyError, arg:
            print 'Error: brakujący klucz (',arg,'). Dane źle wczytane?'

    imageFilename = property( lambda self: self.__imageFilename )
    texture = property( lambda self: self.__texture )
    duration = property( lambda self: self.__duration )
    framesCount = property( lambda self: self.__frameCount )
