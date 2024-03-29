#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Moduł zawiera klasę bazową dla wszystkich strategii oraz kilka przykładowych implementacji. '''

import config

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


from math import cos,sin

class MoveAIStrategy(AIStrategy):
    ''' Przykładowa strategia powodująca ruch obiektu.'''
    def __init__(self, gameObject, spriteStrategy):
        AIStrategy.__init__(self, gameObject, spriteStrategy)
        self.__timer = 0         # licznik czasu, który upłynął

    def update(self, dt):
        self.__timer+=dt
        self.gameObject.velocity=(cos(self.__timer+1.5)/7,cos(self.__timer)/10.0)


class FunctionMoveAIStrategy(AIStrategy):
    ''' Przykładowa strategia powodująca ruch obiektu. Jako velocityFunction przyjmuje
    jednoargumentową funkcję prędkości od czasu. velocityFunction musi zwracać
    parę (xvelocity,yvelocity).'''
    def __init__(self, gameObject, spriteStrategy, velocityFunction):
        AIStrategy.__init__(self, gameObject, spriteStrategy)
        self.__timer = 0         # licznik czasu, który upłynął
        self.__vFunction = velocityFunction

    def update(self, dt):
        self.__timer += dt
        self.gameObject.velocity = self.__vFunction(self.__timer)


class ScrollAIStrategy(AIStrategy):
    ''' Przykładowa strategia powodująca przewijanie się obiektu na scenie (np. dla górek).'''
    def __init__(self, gameObject, spriteStrategy):
        AIStrategy.__init__(self, gameObject, spriteStrategy)
        self.__timer = 0         # licznik czasu, który upłynął

    def update(self, dt):
        self.__timer+=dt
        self.gameObject.velocity = config.SCROLL_VELOCITY_OBJECT


class GroundMoveAIStrategy(AIStrategy):
    ''' Strategia dla pojazdów poruszających się po ziemi.'''
    def __init__(self,gameObject,spriteStrategy,xvelocity):
        AIStrategy.__init__(self,gameObject, spriteStrategy)
        self.gameObject.velocity = (xvelocity, 0)

    def update(self,dt):
        pass
