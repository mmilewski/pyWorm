#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from aiStrategy import DumbAIStrategy
from sceneryObject import SceneryObject, SceneryObjectCreator


class Hill(SceneryObject):
    def __init__(self):
        SceneryObject.__init__(self)

    def clone(self):
        hill = Hill()
        self.clone_base(hill)
        return hill

    def hit(self, damage):
        pass
#         if damage > 0:
#             self.destroy()

class HillCreator(SceneryObjectCreator):
    def __init__(self, spriteManager):
        SceneryObjectCreator.__init__(self, spriteManager)

    def create_object(self):
        self.object = Hill()

    def create_ai_strategy(self):
        self.aiStrategy = DumbAIStrategy(self.object, self.spriteStrategy)
