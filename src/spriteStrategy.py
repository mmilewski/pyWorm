#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spriteScript import SpriteScript, SpriteAnimation


class SpriteStrategy( object ):

    def __init__(self):
        pass

    def update(self, dt):
        abstract


class SpriteScriptStrategy( SpriteStrategy ):

    def __init__(self, spriteScript):
        self.__spriteScript = spriteScript

        # jako animację pobierz domyślną
        self.__curAnim = self.__spriteScript.get_animation( '' ) 

        # numer aktualnie wyświetlanej klatki
        self.__curFrameNum = 0

        # czas od ostatniej zmiany klatki
        self.__lastChangeTime = 0.0

    def set_animation(self, val): self.__curAnim = self.__spriteScript.get_animation(val)
    anim = property( lambda self: self.__curAnim, set_animation )

    curFrameNum = property( lambda self:self.__curFrameNum )


    def update(self, dt):
        self.__lastChangeTime += dt
        if self.__lastChangeTime > self.anim.duration:
            self.__lastChangeTime = 0.0
            self.__curFrameNum += 1
            self.__curFrameNum %= self.anim.framesCount

