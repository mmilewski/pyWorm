#!/usr/bin/python
# -*- coding: utf-8 -*-


class SpriteAnimationFrame:

    def __init__(self, texture, frameRect ):
        ''' Tworzy klatkę animacji sprite'a.
        texture - tekstura, na której jest klatka do narysowania.
        frameRect - krotka (xLewy, yDół, xPrawy, yGóra) opisując, który fragment
        tekstury należy narysować (gdzie znajduje się klatka).'''
        self.__textureId = textureId
        self.__frameRect = frameRect

    frameRect = property( lambda self: self.__frameRect )
    textureId = property( lambda self: self.__textureId )
