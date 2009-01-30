#!/usr/bin/python
# -*- coding: utf-8 -*-

class AIStrategy(object):

    def __init__(self, gameObject, spriteStrategy):
        self.__gameObject     = gameObject       # refrencja do obiektu, którym strategia zarządza
        self.__spriteStrategy = spriteStrategy   # referencja do strategii sprite'a obiektu gameObject


    gameObject = property(lambda self: self.__gameObject)
    spriteStrategy = property(lambda self: self.__spriteStrategy)    
        
        
    def update(self, dt): abstract
    ''' Metoda uaktualniająca stan obiektu.
        dt: czas jaki upłynął od ostatniego uruchomienia tej metody '''

    def set_game_object(self, gameObject):
        self.__gameObject = gameObject

    def set_sprite_strategy(self, spriteStrategy):
        self.__spriteStrategy = spriteStrategy
        

class DumbAIStrategy(AIStrategy):
    ''' Strategia typu: nic nie rób '''
    
    def __init__(self, gameObject, spriteStrategy):
        AIStrategy.__init__(self, gameObject, spriteStrategy)
                            
    def update(self, dt):
        pass


from math import cos

class MoveAIStrategy(AIStrategy):
    ''' Przykładowa strategia powodująca ruch obiektu.'''
    def __init__(self, gameObject, spriteStrategy):
        AIStrategy.__init__(self, gameObject, spriteStrategy)
        self.__timer = 0         # licznik czasu, który upłynął
                            
    def update(self, dt):
        self.__timer+=dt
        self.gameObject.velocity=(cos(self.__timer+1.5)/7,cos(self.__timer)/10.0)

        
class ScrollAIStrategy(AIStrategy):
    ''' Przykładowa strategia powodująca ruch obiektu.'''
    def __init__(self, gameObject, spriteStrategy):
        AIStrategy.__init__(self, gameObject, spriteStrategy)
        self.__timer = 0         # licznik czasu, który upłynął
                            
    def update(self, dt):
        self.__timer+=dt
        self.gameObject.velocity=(-0.11,0)
