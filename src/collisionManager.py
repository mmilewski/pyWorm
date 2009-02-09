#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("game_objects/") # konieczne do korzystania z game_objectów

from gameObject import GameObject, GameObjectEnemy
from playerGameObject import PlayerGameObject
from groundObject import GroundObject
from sceneryObject import SceneryObject
from rocketGameObject import RocketGameObject



class CollisionManager:
    def __init__(self, spriteManager, gameObjects = []):
        ''' Konstruktor. Można utworzyć z gotową listą obiektów. '''
        self.__objects = gameObjects
        self.__spriteManager = spriteManager

        
    def add_object( self, object ):
        ''' Dodaje obiekt do listy obiektów podlegających testowi kolizji. '''
        assert isinstance( object, GameObject ), "Nieprawidłowy typ"
        self.__objects.append(object)
        

    def remove_object( self, object ):
        ''' Usuwa obiekt z listy obiekt podlegających testowi kolizji. '''
        assert isinstance( object, GameObject ), "Nieprawidłowy typ"
        self.__objects.remove(object)        

        
    def get_colliding_objects( self ):
        ''' Zwaraca listę par kolidujących obiektów (kolidują aabb i perpixel).
        Wynik to lista par obiektów, które spełniają warunek:
           check_aabb_collision(o1,o2) && check_per_pixel_collision(o1,o2). '''
        pairs = []
        for o1 in self.__objects:
            for o2 in self.__objects:
                if o1 != o2:
                    if self.__check_type_collision(o1, o2):
                        if self.__check_aabb_collision(o1,o2):
                            if self.__check_per_pixel_collision(o1,o2):
                                pairs.append( (o1,o2) )
        return pairs


    def __check_type_collision( self, o1, o2 ):
        ''' Sprawdza kolizje po typie obiektów. Niektóre typy nie
        kolidują ze sobą w ogóle (np. przeciwnicy między sobą) '''

        
        # Kolizje między graczem a przeciwnikiem
        if isinstance( o1, PlayerGameObject ) and isinstance( o2, GameObjectEnemy ):
            return True

        if isinstance( o1, GameObjectEnemy ) and isinstance( o2, PlayerGameObject ):
            return True

        # Rakiety kolidują ze wszystkim
        if isinstance( o1, RocketGameObject ) or isinstance( o2, RocketGameObject ):
            return True
        
        return False

    
    
    def __check_aabb_collision( self, o1, o2 ):
        ''' Sprawdza czy aabb, obiektów przekazanaych w argumentach, przecinają się. '''
        assert isinstance( o1, GameObject ) and \
            isinstance( o2, GameObject), "Niepoprawny typ"

        (x1, y1, w1, h1) = self.__spriteManager.get_aabb(o1.spriteName, o1.get_current_animation_name(), o1.get_current_frame_num())
        (x2, y2, w2, h2) = self.__spriteManager.get_aabb(o2.spriteName, o2.get_current_animation_name(), o2.get_current_frame_num())

        dx1, dy1 = o1.get_pos()
        dx2, dy2 = o2.get_pos()
        x1 += dx1
        y1 += dy1
        x2 += dx2
        y2 += dy2

        x1 *= 1000 # 800
        x2 *= 1000 # 800
        y1 *= 750  # 600
        y2 *= 750  # 600

        isCollision = True
        if y2 + h2 < y1: isCollision = False
        if y1 + h1 < y2: isCollision = False
        if x2 + w2 < x1: isCollision = False
        if x1 + w1 < x2: isCollision = False
            
        return isCollision

    
    def __check_per_pixel_collision( self, o1, o2 ):
        ''' Sprawdza czy obiekty zadane w argumentach kolidują per-pixel.
        Sprawdzenie kolizji jest delegowane do SpriteManagera. '''
        assert isinstance( o1, GameObject ) and \
            isinstance( o2, GameObject), "Niepoprawny typ"

        return self.__spriteManager.check_per_pixel_collision(o1, o2)
