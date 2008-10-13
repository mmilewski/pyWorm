#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from gameObject import GameObject, GameObjectEnemy, GameObjectCreator
from aiStrategy import AIStrategy
from playerGameObject import PlayerGameObject


class RocketGameObject(GameObject):
    '''
    Zwykła rakieta
    '''
    def __init__(self):
        ''' target: 'player' lub 'enemy'. Określa z czym rakieta koliduje '''
        GameObject.__init__(self)
        self.__target = None       # W co powinna trafić. Możliwe wartości to: 'player' i 'enemy'
        self.__damage = 2          # Obrażenia zadawane przez rakietę


    def get_damage(self):
        return self.__damage

    
    def set_damage(self, value):
        self.__damage = value
        
        
    def set_target(self, target):
        self.__target = target
        

    def get_target(self):
        return self.__target

    
    def clone(self):
        rocket = RocketGameObject()
        self.clone_base(rocket)        
        return rocket

    
    def hit(self, damage):
        if damage > 0:
            self.destroy()
            
    
    def collide(self, object, depth = 0):
        ''' Obsługa kolizji '''

        # sprawdź czy przypadkiem nie ma cyklu w wywołaniach collide
        if depth > 1:
            print 'Błąd: nie umiem obsłużyć kolizji: ', self, ' - ', object
            return
        
        processed = False

        # sprawdzanie kolizji rakieta - rakieta
        if isinstance(object, RocketGameObject):
            if object.get_target() != self.get_target():
                object.hit(1)
                self.hit(1)
            processed = True

        # sprawdzanie kolizji rakieta_na_przeciwnika - nie rakieta
        elif self.__target == 'enemy':
            if isinstance(object, GameObjectEnemy):
                object.hit(self.__damage)
                self.hit(1)
                processed = True

            if isinstance(object, PlayerGameObject):
                processed = True

        # sprawdzanie kolizji rakieta_na_gracza - nie rakieta
        elif self.__target == 'player':
            if isinstance(object, PlayerGameObject):
                object.hit(self.__damage)
                self.hit(1)
                processed = True

            if isinstance(object, GameObjectEnemy):
                processed = True

        # jeżeli nie umiesz obsłużyć kolizji to może drugi obiekt umie
        if not processed:
            object.collide(self, depth + 1)

        
class RocketSimpleAIStrategy(AIStrategy):
    ''' Z założenia dla rakiety może być wiele strategii (np. rakiety
    naprowadzane na najbliższy cel, naprowadzane na zadany cel
    itp). Ta strategi to rakieta, która leci zgodnie z zadanym na
    początku wektorem (czyli leci po linii prostej, w zadanym
    kierunku) '''

    def __init__(self, gameObject, spriteStrategy):
        AIStrategy.__init__(self, gameObject, spriteStrategy)

    def update(self, dt):
        (xPos, yPos) = self.gameObject.position
        
        if xPos >= 1: self.gameObject.destroy()
        if xPos <= 0: self.gameObject.destroy()
        if yPos >= 1: self.gameObject.destroy()
        if yPos <= 0: self.gameObject.destroy()


class SimpleRocketCreator(GameObjectCreator):
    def __init__(self, spriteManager):
        GameObjectCreator.__init__(self, spriteManager)

    def create_object(self):
        self.object = RocketGameObject()

    def create_ai_strategy(self):
        self.aiStrategy = RocketSimpleAIStrategy( self.object, self.spriteStrategy )
