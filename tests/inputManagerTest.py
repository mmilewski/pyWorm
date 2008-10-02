#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../src")

from inputManager import InputManager
from inputManager import InputObserver

import pyglet
from pyglet.window import Window

#
# Obiekt obserwujący wejście
#
class ConcreteInputObserver(InputObserver):
    def __init__(self, name):
        self.__name = name;
    
    # musi idefiniować notify_input jako argument dostaje referencję
    # do InputManagera
    def notify_input(self, subject):
        print "Wejście przechwycone przez: ", self.__name

        ##
        ## UWAGA:
        ##      Ta klasa nie zwraca informacji czy był ostatnio
        ##      naciśnięty puszczony klawisz, tylko jaki jest jego
        ##      stan w danej chilwli. Powiadomienie jest po to, żeby
        ##      sprawdzać stan tylko gdy jest to potrzebne
        ##
        ##      Lista klawiszy o które można pytać jest w pliku
        ##      src/inputKeysMapping.py
        ##      

        print
# WSAD        
        # najpierw pytamy 'subject' o stan klawisza
        state = subject.get_key_state("w");
        # a następnie korzystamy z tej wiedzy
        if state:
            print "\tw is pushed"
        if not state:
            print "\tw is released"

        state = subject.get_key_state("s");
        if state:
            print "\ts is pushed"
        if not state:
            print "\ts is released"

        state = subject.get_key_state("a");
        if state:
            print "\ta is pushed"
        if not state:
            print "\ta is released"
            
        state = subject.get_key_state("d");
        if state:
            print "\td is pushed"
        if not state:
            print "\td is released"

# STRZAŁKI
        print
        state = subject.get_key_state("left");
        if state:
            print "\tleft is pushed"
        if not state:
            print "\tleft is released"

        state = subject.get_key_state("right");
        if state:
            print "\tright is pushed"
        if not state:
            print "\tright is released"

        state = subject.get_key_state("up");
        if state:
            print "\tup is pushed"
        if not state:
            print "\tup is released"
            
        state = subject.get_key_state("down");
        if state:
            print "\tdown is pushed"
        if not state:
            print "\tdown is released"
            
# SPACJA
        print
        state = subject.get_key_state("space");
        if state:
            print "\tspace is pushed"
        if not state:
            print "\tspace is released"

# Utworzenie InputManagera i włączenie go do pygleta            
manager = InputManager()
window = Window()
window.on_key_press = lambda symbol, modifiers: manager.key_pressed(symbol, modifiers)
window.on_key_release = lambda symbol, modifiers: manager.key_released(symbol, modifiers)

# Tworzymy 3 obiekty obserwujące
ops1 = ConcreteInputObserver('ops1')
ops2 = ConcreteInputObserver('ops2')
ops3 = ConcreteInputObserver('ops3')

# dodajemy obserwatorów
manager.register_observer(ops1)
manager.register_observer(ops2)
manager.register_observer(ops3)

# usuwamy obserwatorów
manager.unregister_observer(ops1)
manager.unregister_observer(ops2) 

# zostaje tylko trzech obserwatorów
# uruchamiamy aplikację
print "Możesz sprawdzić działanie klawszy wsad, strzałek oraz spacji"
window.clear()
pyglet.app.run()
