#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from aiStrategy import GroundMoveAIStrategy
from gameObject import GameObjectEnemy, GameObjectCreator


class Tank1(GameObjectEnemy):
    def __init__(self):
        GameObjectEnemy.__init__(self)

    def clone(self):
        tank = Tank1()
        self.clone_base(tank)
        return tank

    def hit(self, damage):
        if damage > 0:
            self.destroy()
        
class Tank1Creator(GameObjectCreator):
    def __init__(self, spriteManager):
        GameObjectCreator.__init__(self, spriteManager)

    def create_object(self):
        self.object = Tank1()

    def create_ai_strategy(self):
        self.aiStrategy = GroundMoveAIStrategy( self.object, self.spriteStrategy, -0.15 )
