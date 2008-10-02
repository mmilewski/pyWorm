#!/usr/bin/env python
# -*- coding: utf-8 -*-

from inputKeysMapping import pyglet_key_mapping
from inputKeysMapping import pyglet_shift_code, pyglet_capslock_code

class InputObserver(object):

    def notify_input(self, subject): abstract

##
## FIXME: 'A' i 'a' powinny być równoznaczne, podczas gdy nie ma
## możliwości obsługi (jakiejkolwiek) 'A'. Wygląda to na błąd w
## bibliotece pyglet
##
class InputManager(object):

    def __init__(self):
        # lista obiektów obserwujących wejście
        self.__observers = []

        # tłumaczenie klawiszy z pyglet'a na format pyWorm (stringi)
        self.__key_codes = pyglet_key_mapping

        # stan klawiszy. dla każdego jest pamięta true (wciśnięty) lub false (puszczony)
        self.__keys_state = {}
        for key_code in self.__key_codes.values():
            self.__keys_state[key_code] = False

            
    def key_pressed(self, symbol, modifier):
        # Niestety pyglet robi dziwne rzeczy przy kombinacji shift + litera
        if modifier & pyglet_shift_code or modifier & pyglet_capslock_code: return
        
        if not self.__assert(self.__key_codes.has_key(symbol), "Nieznany symbol klawisza"): return
        if self.__key_codes.has_key(symbol):
            self.__keys_state[ self.__key_symbol_to_string(symbol) ] = True
        self.__notify()

        
    def key_released(self, symbol, modifier):
        # Niestety pyglet robi dziwne rzeczy przy kombinacji shift + litera        
        if modifier & pyglet_shift_code or modifier & pyglet_capslock_code: return
        
        if not self.__assert(self.__key_codes.has_key(symbol), "Nieznany symbol klawisza"): return        
        if self.__key_codes.has_key(symbol):        
            self.__keys_state[ self.__key_symbol_to_string(symbol) ] = False
        self.__notify()

        
    def register_observer(self, observer):
        if isinstance(observer, InputObserver) and not observer in self.__observers:
            self.__observers.append(observer)

            
    def unregister_observer(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

            
    def get_key_state(self, keyname):
        if not self.__assert(self.__keys_state.has_key(keyname), "Nieznana nazwa klawisza: " + keyname): return False
        return self.__keys_state[keyname]

    
    def __key_symbol_to_string(self, symbol):
        return self.__key_codes[symbol]

    
    def __notify(self):
        for obj in self.__observers:
            obj.notify_input(self)

    #
    # W rc wystarczy zakomentować pierwszą linię tej funkcji.
    # Działanie będzie takie, że tam gdzie byłby błąd, funkcja
    # zakończy działanie (ignorowanie błędu.
    #
    def __assert(self, condition, desc):
        assert condition, desc
        return condition

