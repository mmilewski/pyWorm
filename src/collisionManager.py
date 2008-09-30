#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gameObject import GameObject

class CollisionManager:
    def __init__(self, gameObjects=[]):
        ''' Konstruktor. Można utworzyć z gotową listą obiektów. '''
        self.__objects = gameObjects

    def add_object( self, object ):
        ''' Dodaje obiekt do listy obiektów podlegających testowi kolizji. '''
        assert isinstance( object, GameObject ), "Nieprawidłowy typ"

    def remove_object( self, object ):
        ''' Usuwa obiekt z listy obiekt podlegających testowi kolizji. '''
        assert isinstance( object, GameObject ), "Nieprawidłowy typ"

    def get_colliding_objects( self ):
        ''' Zwaraca listę par kolidujących obiektów (kolidują aabb i perpixel).
        Wynik to lista par obiektów, które spełniają warunek:
           check_aabb_collision(o1,o2) && check_per_pixel_collision(o1,o2). '''
        pairs = []
        for o1 in self.__objects:
            for o2 in self.__objects:
                if self.__check_aabb_collision(o1,o2):
                    if self.__check_per_pixel_collision(o1,o2):
                        pairs.append( (o1,o2) )
        return pairs

    def __check_aabb_collision( self, o1, o2 ):
        ''' Sprawdza czy aabb, obiektów przekazanaych w argumentach, przecinają się. '''
        assert isinstance( o1, GameObject ) and \
            isinsance( o2, GameObject), "Niepoprawny typ"
        return False

    def __check_per_pixel_collision( self, o1, o2 ):
        ''' Sprawdza czy obiekty zadane w argumentach kolidują per-pixel.
        Sprawdzenie kolizji jest delegowane do SpriteManagera. '''
        assert isinstance( o1, GameObject ) and \
            isinsance( o2, GameObject), "Niepoprawny typ"

        return False


class SpriteManager:
    def __init__(self):
        pass

    def check_sprite_collision( self, spriteName1, spriteName2, delta ):
        ''' Sprawdza czy jeżeli na sprite1 nałożymy sprite2 w pozycji delta
        (jest to przesunięcie lewego dolnego rogu sprite2 względem lewego dolnego
        rogu sprite1), to czy istnieją dwa pikesele które nachodzą na siebie
        (czyli czy przecięcie miejsc gdzie oba nie mają kanału alfa 0 jest niepuste). '''
        assert len(delta)==2 \
            and isinsance(spriteName1,str) \
            and isinsance(spriteName2,str), \
            "Warning, prawdopodobnie zły typ argumentu. "



### TESTS ###
