#!/usr/bin/python
# -*- coding: utf-8 -*-


class GameObjectFactory(object):

    def __init__(self):
        # obiekty  { string:obiekt }
        self.__objects = {}


    def create_object(self, objectName):
        ''' Tworzy obiekt na podstawie nazwy.
        Jeżeli nie znaleziono obiektu, to zwraca None. '''
        print "GameObjectFactory:",
        if self.__objects.has_key(objectName):
            print "Tworzenie obiektu `%s`" % objectName
            return self.__objects[objectName].clone()
        else:
            print "WARNING, obiektu `%s` nie znaleziono, nie utworzono." % objectName
            return None


    def register_game_object(self, object, name):
        ''' Dodaje obiekt do fabryki. Zgłasza próbę ponownego rejestrowania. '''
        print "GameObjectFactory:",
        if not object:
            print "WARNING, próba zarejestrowania pustego obiektu `%s`"%name
            return
        if self.__objects.has_key(name):
            print "WARNING, ponowne rejestrowanie `%s`"%name
            self.__objects[name] = object.clone()
        else:
            print "zarejestrowano `%s`"%name
            self.__objects[name] = object.clone()
