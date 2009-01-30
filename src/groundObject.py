#!/usr/bin/python
# -*- coding: utf-8 -*-

from gameObject import GameObject,GameObjectCreator


class GroundObjectCreator(GameObjectCreator):
    def __init__(self, spriteManager):
        GameObjectCreator.__init__(self,spriteManager)


class GroundObject(GameObject):
    def __init__(self):
        GameObject.__init__(self)

