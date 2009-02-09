#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from aiStrategy import DumbAIStrategy, MoveAIStrategy, FunctionMoveAIStrategy
from gameObject import GameObjectEnemy, GameObjectCreator

import config
from math import cos

class Helicopter1(GameObjectEnemy):
    def __init__(self):
        GameObjectEnemy.__init__(self)

    def clone(self):
        heli = Helicopter1()
        self.clone_base(heli)
        return heli

    def hit(self, damage):
        if damage > 0:
            self.destroy()

class Helicopter1Creator(GameObjectCreator):
    def __init__(self, spriteManager):
        GameObjectCreator.__init__(self, spriteManager)

    def create_object(self):
        self.object = Helicopter1()

    def create_ai_strategy(self):
#         self.aiStrategy = DumbAIStrategy(self.object, self.spriteStrategy)
#         self.aiStrategy = MoveAIStrategy(self.object, self.spriteStrategy)
        scrollx = config.SCROLL_VELOCITY_OBJECT[0]
        f=lambda t: ( scrollx-.05, cos(t*3)/6.0 )
        self.aiStrategy = FunctionMoveAIStrategy(self.object, self.spriteStrategy,f)
