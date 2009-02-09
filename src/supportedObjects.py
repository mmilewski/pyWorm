#!/usr/bin/python
# -*- coding: utf-8 -*-


''' W tym pliku jest definicja tylko jednej funkcji. Jest to funkcja
tworząca prototypy wszystkich możliwych obiektów w grze. Należy ją
modyfikować (dodawać nowe wiersze) zawsze gdy jest potrzeba dodania
nowego prototypu do gry.'''


from helicopter1 import Helicopter1Creator
from helicopter1a import Helicopter1aCreator
from hill import HillCreator
from stone import StoneCreator
from grass import GrassCreator
from bridge import BridgeCreator
from tank1 import Tank1Creator
from pipe1 import Pipe1Creator
from cannon import CannonCreator

def add_supported_objects_to_factory(objFactory, spriteManager):

    # definicja pomocniczej funkcji dodającej obiekt
    def add_object(objFactory, name, creator):
        obj = creator.create( name )
        objFactory.register_game_object( obj, name )

    # Dodawanie obiektów
    add_object(objFactory, 'helicopter1', Helicopter1Creator(spriteManager))
    add_object(objFactory, 'helicopter1a', Helicopter1aCreator(spriteManager))
    add_object(objFactory, 'tank1', Tank1Creator(spriteManager))
    add_object(objFactory, 'pipe1', Pipe1Creator(spriteManager))
    add_object(objFactory, 'cannon', CannonCreator(spriteManager))

    # sceneria
    add_object( objFactory, 'hill', HillCreator(spriteManager))

    # podłoże
    add_object( objFactory, 'stone', StoneCreator(spriteManager))
    add_object( objFactory, 'grass', GrassCreator(spriteManager))
    add_object( objFactory, 'bridge', BridgeCreator(spriteManager))
