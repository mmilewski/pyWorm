#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet import image
from spriteScript import SpriteScript

class SpriteFrame:

    def __init__(self, texture, frameRect ):
        ''' Tworzy klatkę.
        texture - tekstura, na której jest klatka do narysowania.
        frameRect - krotka (xLewy, yDół, xPrawy, yGóra) opisując, który fragment
        tekstury należy narysować (gdzie znajduje się klatka).'''
        self.__texture = texture
        self.__frameRect = frameRect

    rect = property( lambda self: self.__frameRect )
    texture = property( lambda self: self.__texture )



class SpriteManager:

    def __init__(self):
        # słownik ze sprite'ami (nazwaSprite'a, script)
        self.__sprites = {}

        # rozszerzenie dla plików z definicją sprite'a
        self.__spriteExtension = '.sprite'

    spriteExt = property( lambda self: self.__spriteExtension )


#     def load_sprite_from_file(self, filename):
#         ''' Ładuje sprite'a z pliku skryptowego. '''
#         s = SpriteScript()
#         s.load_from_file(filename)
#         self.add_script( ..... )


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
        # ADDME
        # wyliczenie współrzednych klatki do narysowania
        #
        imageFilename = (self.__sprites[spriteName]).imageFilename
        tex = image.load(imageFilename).get_texture()
        return SpriteFrame( tex, (0,0,1,1) )
