#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path              # join, isfile
import levelParser

class LevelManager(object):
    ''' Zadaniem zarządcy poziomu jest załadowanie poziomu, a
    następnie dorzucanie go gameWorld obiektów w odpowiednim
    czasie. Między innymi powinien też tworzyć tło. Nie powinien
    zarządzać instancjami gracza, gdyż tym zajmuje się gameWorld '''

    def __init__(self, objectFactory):
        ''' objectFactory: Fabryka wykorzystywana do tworzenia obiektów (głównie przeciwników) '''
        self.__objectFactory = objectFactory                # fabryka obiektów
        self.__screenResolution = 100     # rozdzielczość ekranu w pewnych jednostkach (żeby uciec od pikseli)
        self.__scrollSpeed = 0.333        # prędkość przesuwania ekranu = 1/3 ekranu na sekundę
        self.__creatorPos = self.__screenResolution   # wartość rozdzielająca istniejące obiekty od jeszcze niestworzonych
        self.__prevCreatorPos = 0         # pozycja poprzedniego tworzyciela

    def load_level(self, levelName):
        ''' Zmienia poziom na `levelName`. `levelName + 'lvl'` musi być nazwą poziomu występującą w `levels/`.
        Zwraca status powodzenia, True-załadowano poprawnie, False-wystąpił błąd.'''
        print 'Ładowanie poziomu `%s`' % levelName
        filename = os.path.join( '..', 'levels', levelName + '.lvl')
        if not os.path.isfile( filename ):
            print "Brak pliku z poziomem, szukano %s" % filename
            return False

        parser = levelParser.LevelParser( filename )
        errors = parser.get_errors()
        if errors:
            print len(errors), "Błędy podczas tworzenia pasera poziomu:"
            for error in errors:
                print "\t", error
            return False

        # obiekty gry
        self.__objectManager = parser.get_object_manager()
        self.__levelObjects = self.__objectManager.get_all_objects()

        # tła
        self.__backgroundManager = parser.get_background_manager()

        # elementy pejzażu
        self.__sceObjectManager = parser.get_sce_manager()
        self.__sceObjects = self.__sceObjectManager.get_all_objects()

        return True


    def get_background_filenames(self):
        fs = self.__backgroundManager.get_filenames()
        assert len(fs)>0, "Brak plików z tłami."
        return fs


    def update(self, dt, gameWorld):
        ''' Aktualizuje menedżer o czas dt udostępniając świat, aby można było dodać obiekty. '''

        # przesuń tworzyciela
        prevCreatorPos=self.__creatorPos
        self.__creatorPos += dt * self.__scrollSpeed * self.__screenResolution

        # dodaj obiekty do świata, jeżeli nadszedł na nie czas
        delete_counter = 0                                     # liczba obiektów do usunięcia z początku listy
        for object in self.__levelObjects:
            if object.get_position_x() > self.__creatorPos:    # twórz dopóki obiekty są przed tworzycielem
                break
            delete_counter += 1
            obj = self.__objectFactory.create_object( object.get_name() )  # utwórz obiekt fabryką
            if obj:
                obj.position = object.get_screen_position()                # ustaw pola
                gameWorld.add_object( obj )                                # i dodaj od świata
        self.__levelObjects = self.__levelObjects[ delete_counter : ]

        # dodaj obiekty do świata, jeżeli nadszedł na nie czas
        delete_counter = 0                                     # liczba obiektów do usunięcia z początku listy
        for object in self.__sceObjects:
            if object.get_position_x() > self.__creatorPos:    # twórz dopóki obiekty są przed tworzycielem
                break
            delete_counter += 1
            obj = self.__objectFactory.create_object( object.get_name() )   # utwórz obiekt fabryką
            if obj:
                obj.position = object.get_screen_position()                 # ustaw pola
                gameWorld.add_object( obj )                                 # i dodaj od świata
        self.__sceObjects = self.__sceObjects[ delete_counter : ]


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

