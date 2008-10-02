#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spriteScript import SpriteScript, SpriteAnimation
from math import floor


class SpriteStrategy( object ):

    def __init__(self):
        pass


    def get_animation_name(self): abstract
    def get_frame_duration(self): abstract
    def get_current_frame_num(self): abstract
    def get_animation_duration(self): abstract

    def set_animation(self, animName, frameDuration, startFrame): abstract

    def update(self, dt):
        abstract


class SpriteScriptStrategy( SpriteStrategy ):

    def __init__(self, spriteScript):

        # zapamiętaj dane ze skryptu
        self.__spriteScript = spriteScript

        # nazwa aktualnie przetwarzanej animacji
        self.__animationName = ''  # domyślna

        # ustaw aktualną animację na domyślną
        self.__curAnimation = self.__spriteScript.get_animation(self.__animationName)

        # czas trwania animacji (o ile klatki animacja zaczęła się od 0. klatki)
        self.__animationDuration = 0.0

    def get_animation_name(self): return self.__animationName
    def get_current_frame_num(self):
        return floor(self.get_animation_duration()/self.__curAnimation.duration)

    #
    # FIXME klasy pochodne nie muszą wcale dostarczać propercji
    #
    animationName = property( get_animation_name )
    frameDuration = property( get_frame_duration )
    currentFrameNum = property( get_current_frame_num )
    animationDuration = property( get_animation_duration )


    def set_animation(self, animName, startFrame=0):
        animation = self.__spriteScript.get_animation( animName )
        if not animation:  # jeżeli nie ma animacji, to załaduj domyślną
            self.__animationName = ''
            animation = self.__spriteScript.get_animation( '' )
            if not animation: # jeżeli nie ma domyślnej, to spanikuj
                print 'PANIC: Brak domyślnej animacji. Próbowano ustawić `%s`'%animName
        else:
            self.__animationName = animName
        self.__curAnimation = animation

        frameDuration = self.__curAnimation.duration
        self.__animationDuration = 0.0 + frameDuration * startFrame
        self.__curFrameNum = startFrame


    def update(self, dt):
        self.__animationDuration += dt
