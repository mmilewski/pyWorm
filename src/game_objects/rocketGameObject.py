#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from copy import deepcopy

from gameObject import GameObject, GameObjectCreator
from aiStrategy import AIStrategy


class RocketGameObject(GameObject):
    '''
    Zwykła rakieta
    '''
    def __init__(self):
        ''' target: 'player' lub 'enemy'. Określa z czym rakieta koliduje '''
        GameObject.__init__(self)
        self.__target = None       # W co powinna trafić. Możliwe wartości to: 'player' i 'enemy'

    def set_target(self, target):
        self.__target = target
        
    def clone(self):
        rocket = RocketGameObject()
        
        rocket.aabb           = self.aabb
        rocket.spriteName     = self.spriteName
        rocket.position       = self.position
        rocket.velocity       = self.velocity
        rocket.spriteStrategy = deepcopy(self.spriteStrategy)
        rocket.aiStrategy     = deepcopy(self.aiStrategy)
        rocket.aiStrategy.set_game_object(rocket)
        
        return rocket
    
    def collide(self, object):
        pass


class RocketSimpleAIStrategy(AIStrategy):
    ''' Z założenia dla rakiety może być wiele strategii (np. rakiety
    naprowadzane na najbliższy cel, naprowadzane na zadany cel
    itp). Ta strategi to rakieta, która leci zgodnie z zadanym na
    początku wektorem (czyli leci po linii prostej, w zadanym
    kierunku) '''

    def __init__(self, gameObject, spriteStrategy):
        self.__gameObject     = gameObject       # refrencja do obiektu, którym strategia zarządza
        self.__spriteStrategy = spriteStrategy   # referencja do strategii sprite'a obiektu gameObject


    def set_game_object(self, gameObject):
        self.__gameObject = gameObject

    def set_sprite_strategy(self, spriteStrategy):
        self.__spriteStrategy = spriteStrategy
        
    def update(self, dt):
        (xPos, yPos) =  self.__gameObject.position
        
        if xPos >= 1: self.__gameObject.destroy()
        if xPos <= 0: self.__gameObject.destroy()
        if yPos >= 1: self.__gameObject.destroy()
        if yPos <= 0: self.__gameObject.destroy()


class SimpleRocketCreator(GameObjectCreator):
    def __init__(self, spriteManager):
        GameObjectCreator.__init__(self, spriteManager)

    def create_object(self):
        self.object = RocketGameObject()

    def create_ai_strategy(self):
        self.aiStrategy = RocketSimpleAIStrategy( self.object, self.spriteStrategy )
