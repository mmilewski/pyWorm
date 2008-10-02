#!/usr/bin/python
# -*- coding: utf-8 -*-



class AnimationInfo(object):

    def __init(self, xOffset, yOffset, frameW, frameH, colsCount, framesCount):
        self.__offset = (xOffset,yOffset)
        self.__frameSize = (frameW, frameH)
        self.__colsCount = colsCount
        self.__frameSize = framesCount


class SpriteInfo(object):

    def __init__(self, textureId, animations={}):

        # id tekstury dla sprite'a
        self.__textureId = textureId

        # animacje dostępne w sprite'cie
        # dict( nazwaAnimacji : animationInfo )
        self.__animations = animations

