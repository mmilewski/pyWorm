#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Moduł zawiera reprezentację obiektu sceny.'''

from gameObject import GameObject,GameObjectCreator


class SceneryObjectCreator(GameObjectCreator):
    def __init__(self, spriteManager):
        GameObjectCreator.__init__(self,spriteManager)


class SceneryObject(GameObject):
    def __init__(self):
        GameObject.__init__(self)

