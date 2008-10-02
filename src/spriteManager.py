#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet import image
# from spriteScript import SpriteScript
from spriteInfo import SpriteInfo
from spriteAnimationFrame import SpriteAniamtionFrame


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

        #
        # FIXME
        # wyliczenie współrzednych klatki do narysowania
        #

        imageFilename = (self.__sprites[spriteName]).imageFilename
        tex = image.load(imageFilename).get_texture()
        return SpriteAnimationFrame( tex, (0,0,1,1) )


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
