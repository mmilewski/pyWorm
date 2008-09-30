#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spriteScript import SpriteScript
from spriteStrategy import SpriteScriptStrategy


class GameObject(object):

    def __init__(self):
        # krotka (pozycjaX,pozycjaY,szerokość, wysokość)
        self._aabb = None

        # nazwa sprit'a przypisana do obiektu
        self._spriteName = ''

        # strategia wykorzystywana przez obiekt
        # (GameObjectAIStrategy)
        self._aiStrategy = None

        # strategia zarządzająca stanem animacji
        # (SpriteStrategy)
        self._spriteStrategy = None


    def set_aabb(self,val): self._aabb = val
    aabb = property(lambda self:self._aabb, set_aabb )

    def set_sprite_name(self,val): self._spriteName = val
    spriteName = property(lambda self: self._spriteName, set_sprite_name)

    def set_ai_strategy(self,val): self._aiStrategy = val
    aiStrategy = property( None, set_ai_strategy)

    def set_sprite_strategy(self,val): self._spriteStrategy = val
    spriteStrategy = property( lambda self:self._spriteStrategy, set_sprite_strategy)


    def clone():
        abstract


    def update(self, dt):
        abstract



class Triangle(GameObject):

    def __init__(self):
        GameObject.__init__(self)
        self.__rot = 0.0


    def clone(self):
        return Triangle()


    def update(self,dt):
        self.__rot = self.__rot + dt
        if self._spriteStrategy:
            self._spriteStrategy.update( dt )
        else:
            print 'Error: ups, no scriptStrategy assigned.',self.__class__
#         print "Triangle update:", self.__rot

