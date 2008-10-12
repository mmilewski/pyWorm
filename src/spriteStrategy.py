#!/usr/bin/env python
# -*- coding: utf-8 -*-


from math import floor


class SpriteScriptStrategy( object ):
    ''' Sterowanie logiką sprite'a (zmiany stanu animacji - klatek) '''

    def __init__(self, spriteScript):
        self.__spriteScript = spriteScript        # zapamiętaj dane ze skryptu
        self.__animationName = 'default'          # nazwa aktualnie przetwarzanej animacji
        self.__animationDuration = 0.0            # czas trwania animacji
        self.__animationDurationDivisor = 1000.0  # liczba jaka odpowiada jednej sekundzie
        self.__lastFinishedAnimationName = None   # animacja, która jako ostatnia została zakończona


    def get_animation_name(self):
        return self.__animationName

    
    def get_current_frame_num(self):
        animation = self.__spriteScript[ self.__animationName ]
        val = int(floor((self.__animationDuration / (animation.duration / self.__animationDurationDivisor)) * animation.frames_count))
        return val

    
    def set_animation(self, animName):
        self.__animationName = animName
        self.__curFrameNum   = 0
        self.__animationDuration = 0.0

        
    def update(self, dt):
        self.__animationDuration += dt

        animation = self.__spriteScript[ self.__animationName ]
        animationFinished = False
        while self.__animationDuration >= animation.duration / self.__animationDurationDivisor:
            self.__animationDuration -= animation.duration / self.__animationDurationDivisor
            animationFinished = True

        if animationFinished:
            self.__finish_current_animation()


    #
    # Zarządzanie informacjami o zakończonych animacjach
    #
    # Nie należy polegać na obecnych implementacjach tych metod (w
    # tym przypadku szczególnie) - mogą się znacznie zmienić.
    # 
            
    def clear_finished_animation(self):
        self.__lastFinishedAnimationName = None

    def get_last_finished_animation_name(self):
        return self.__lastFinishedAnimationName
        
    def __finish_current_animation(self):
        self.__lastFinishedAnimationName = self.__animationName

