#!/usr/bin/python
# -*- coding: utf-8 -*-


from pyglet.gl import glIsTexture


class SpriteAnimationFrame:

    def __init__(self, textureId, drawRect ):
        ''' Tworzy klatkę animacji sprite'a.
        texture - tekstura, na której jest klatka do narysowania.
        drawRect - krotka (xLewy, yDół, xPrawy, yGóra) opisując, który fragment
        tekstury należy narysować (gdzie znajduje się klatka).'''
        self.__textureId = textureId
        if not glIsTexture(self.textureId):
            print "WARNING: tworzenie SpriteAnimationFrame z nieprawidłowym id tekstury."
        self.__rect = drawRect

    rect = property( lambda self: self.__rect )
    textureId = property( lambda self: self.__textureId )
