#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# W tym pliku jest definicja tylko jednej funkcji. Jest to funkcja
# tworząca prototypy wszystkich możliwych obiektów w grze. Należy ją
# modyfikować (dodawać nowe wiersze) zawsze gdy jest potrzeba dodania
# nowego prototypu do gry
#

import sys
sys.path.append("../")

from helicopter1 import Helicopter1Creator


def add_supported_objects_to_factory(objFactory, spriteManager):

    # definicja pomocniczej funkcji dodającej obiekt
    def add_object(objFactory, name, creator):
        obj = creator.create( name )
        objFactory.register_game_object( obj, name )

    # Dodawanie obiektów
    add_object(objFactory, 'helicopter1', Helicopter1Creator(spriteManager))
