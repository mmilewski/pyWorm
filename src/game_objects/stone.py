#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from aiStrategy import ScrollAIStrategy
from groundObject import GroundObject, GroundObjectCreator


class Stone(GroundObject):
    def __init__(self):
        GroundObject.__init__(self)

    def clone(self):
        stone = Stone()
        self.clone_base(stone)
        return stone

    def hit(self, damage):
        pass
#         if damage > 0:
#             self.destroy()

class StoneCreator(GroundObjectCreator):
    def __init__(self, spriteManager):
        GroundObjectCreator.__init__(self, spriteManager)

    def create_object(self):
        self.object = Stone()

    def create_ai_strategy(self):
        self.aiStrategy = ScrollAIStrategy(self.object, self.spriteStrategy)
