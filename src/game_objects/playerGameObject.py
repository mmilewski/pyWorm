#!/usr/bin/python
# -*- coding: utf-8 -*-

from gameObject import GameObject


class PlayerGameObject(GameObject):
    
    def __init__(self):
        GameObject.__init__(self)
    
    def clone(self):
        raise "Obiektu gracza nie można klonować"

    def hit(self, damage):
        pass

