#!/usr/bin/python
# -*- coding: utf-8 -*-

# from copy import deepcopy
# from spriteStrategy import SpriteScriptStrategy
# from spriteScriptParser import SpriteScriptParser

from gameObject import GameObject,GameObjectCreator


class SceneryObjectCreator(GameObjectCreator):
    def __init__(self, spriteManager):
        GameObjectCreator.__init__(self,spriteManager)


class SceneryObject(GameObject):
    def __init__(self):
        GameObject.__init__(self)

