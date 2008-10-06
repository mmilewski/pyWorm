#!/usr/bin/python
# -*- coding: utf-8 -*-

class LevelManager(object):
    ''' Zadaniem zarządcy poziomu jest załadowanie poziomu, a
    następnie dorzucanie go gameWorld obiektów w odpowiednim
    czasie. Między innymi powinien też tworzyć tło. Nie powinien
    zarządzać instancjami gracza, gdyż tym zajmuje się gameWorld '''

    def __init__(self, objectFactory):
        ''' objectFactory: Fabryka wykorzystywana do tworzenia obiektów (głównie przeciwników) '''
        self.__object_factory = objectFactory

    def load_level(self, levelName):
        ''' zmienia poziom na `levelName`. `levelName + 'lvl'` musi być nazwą poziomu występującą w `levels/`  '''
        print 'Ładowanie poziomu `%s`' % levelName


        #
        # Tu trzeba dodać załadowanie pliku levelName (skryptu)
        # następnie w update będzie wywoływane dodawanie przeciwników
        # do planszy, lub przejście do następnego poziomu
        #
        # Trzeba dodać interfejs typu "level_finishing,
        # level_finished, level_starting, level_started", aby
        # gameWorld wiedział kiedy robić przejścia
        #
        # Musi też być metoda next_level, która przechodzi do następnego poziomu
        # 
