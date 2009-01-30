#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from aiStrategy import ScrollAIStrategy
from groundObject import GroundObject, GroundObjectCreator


class Grass(GroundObject):
    def __init__(self):
        GroundObject.__init__(self)

    def clone(self):
        grass = Grass()
        self.clone_base(grass)
        return grass

    def hit(self, damage):
        pass
#         if damage > 0:
#             self.destroy()

class GrassCreator(GroundObjectCreator):
    def __init__(self, spriteManager):
        GroundObjectCreator.__init__(self, spriteManager)

    def create_object(self):
        self.object = Grass()

    def create_ai_strategy(self):
        self.aiStrategy = ScrollAIStrategy(self.object, self.spriteStrategy)
