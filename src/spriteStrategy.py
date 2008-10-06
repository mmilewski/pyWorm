#!/usr/bin/env python
# -*- coding: utf-8 -*-


from math import floor


class SpriteScriptStrategy( object ):
    ''' Sterowanie logiką sprite'a (zmiany stanu animacji - klatek) '''

    def __init__(self, spriteScript):
        self.__spriteScript = spriteScript        # zapamiętaj dane ze skryptu
        self.__animationName = 'default'          # nazwa aktualnie przetwarzanej animacji
        self.__animationDuration = 0.0            # czas trwania animacji


    def get_animation_name(self):
        return self.__animationName

    
    def get_current_frame_num(self):
        animation = self.__spriteScript[ self.__animationName ]
        val = int(floor((self.__animationDuration / (animation.duration / 100.0)) * animation.frames_count))
        return val

    
    def set_animation(self, animName):
        self.__animationName = animName
        self.__curFrameNum   = 0
        self.__animationDuration = 0.0

        
    def update(self, dt):
        self.__animationDuration += dt

        animation = self.__spriteScript[ self.__animationName ]
        animationFinished = False
        while self.__animationDuration >= animation.duration / 100.0:
            self.__animationDuration -= animation.duration / 100.0
            animationFinished = True

        if animationFinished:
            pass # FIXME: powiadomienie aiStrategy o zakończeniu animacji self.__animationName
