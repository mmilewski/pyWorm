#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet import image
# from spriteScript import SpriteScript
from spriteInfo import SpriteInfo
from spriteAnimationFrame import SpriteAnimationFrame

from pyglet.gl import *  # glIsTexture

class SpriteManager:

    def __init__(self):
        # słownik ze sprite'ami (nazwaSprite'a, script)
        self.__sprites = {}

        # rozszerzenie dla plików z definicją sprite'a
        self.__spriteExtension = '.sprite'

    spriteExt = property( lambda self: self.__spriteExtension )


    def add_script(self, scriptName, spriteScript):
        ''' Dodaje skrypt do menadżera. '''
        # wyluskaj samą nazwę (obetnij rozszerzenie, jeżeli istnieje)
        bareName = scriptName
        if scriptName.endswith(self.spriteExt):
            bareName = scriptName[ :len(scriptName) ]

        print 'DEBUG: SpriteManager: Dodaję skrypt `%s` jako `%s`.' % (scriptName,bareName)
        self.__sprites[bareName] = spriteScript


    def get_frame( self, spriteName, animationName, frameNum ):
        ''' Zwraca klatkę do narysowania.
        spriteName - nazwa sprite z animacją do narysowania
        animationName - nazwa znimacji w sprite'cie do narysowania
        frameNum - numer klatki animacji do narysowania. '''

#         print "Debug: get_frame(`%s`,`%s`,%d)"%(spriteName, animationName, frameNum)

        #
        # FIXME
        # wyliczenie współrzednych klatki do narysowania
        #

        imageFilename = (self.__sprites[spriteName]).imageFilename
        img  = image.load(imageFilename)
        tex = img.get_texture()
        texId = tex.id
#         print "Debug: get_frame ładowanie `%s`"%imageFilename
#         print "Debug: get_frame",img,tex,texId,texId.__class__,tex.target

        if not glIsTexture(texId):
            print "PANIC: nie stworzono tekstury. Problem z ładowaniem obrazka?"

#         #
#         # FIXME
#         # dlaczego tutaj działa a w drawWorld nie??????
#         #
#         glEnable( GL_TEXTURE_2D )
#         glBindTexture( GL_TEXTURE_2D, texId )
#         left,bottom,right,top = 0,0,1,1
#         tc = ( (left,bottom), (right,bottom), (right,top), (left,top) )
#         left,bottom,right,top = .2,.2,.7,.7
#         vs = ( (left,bottom), (right,bottom), (right, top), (left, top) )
#         glBegin( GL_QUADS )
#         for t,v in zip(tc,vs):
#             glTexCoord2f( *t )
#             glVertex2f( *v )
#         glEnd()

        return SpriteAnimationFrame( texId, (0,0,1,1) )


    def check_sprite_collision(self, sprite1, sprite2, delta):
        ''' Sprawdza czy jeżeli na sprite1 nałożymy sprite2 w pozycji delta
        (jest to przesunięcie lewego dolnego rogu sprite2 względem lewego dolnego
        rogu sprite1), to czy istnieją dwa pikesele które nachodzą na siebie
        (czyli czy przecięcie miejsc gdzie oba nie mają kanału alfa 0 jest niepuste). '''

        #
        # FIXME
        # sprawdzanie per-pixel
        #

        return True
