#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Moduł zawiera klasę do obsługu poziomu. Komunikując się z LevelParserem
dodaje do poziomu obiekty w odpowiednim momencie.'''

import os.path              # join, isfile
import levelParser

class LevelManager(object):
    ''' Zadaniem zarządcy poziomu jest załadowanie poziomu, a
    następnie dorzucanie go gameWorld obiektów w odpowiednim
    czasie. Między innymi powinien też tworzyć tło. Nie powinien
    zarządzać instancjami gracza, gdyż tym zajmuje się gameWorld '''

    def __init__(self, objectFactory, spriteManager):
        ''' objectFactory: Fabryka wykorzystywana do tworzenia obiektów (głównie przeciwników) '''
        self.__spriteManager = spriteManager
        self.__objectFactory = objectFactory                # fabryka obiektów
        self.__screenResolution = 100.0   # rozdzielczość ekranu w pewnych jednostkach (żeby uciec od pikseli)
        self.__scrollSpeed = 0.144        # prędkość przesuwania ekranu = 77/1000 ekranu na sekundę
        self.__creatorPos = self.__screenResolution   # wartość rozdzielająca istniejące obiekty od jeszcze niestworzonych
        self.__prevCreatorPos = 0         # pozycja poprzedniego tworzyciela
        self.__window_coords = (1,.75)
        self.__window_draw_dim = (1000,750)

    def set_window_coords(self, coords):
        self.__window_coords = coords

    def set_window_draw_dim(self, dim):
        self.__window_draw_dim = dim

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

        # definicje
        self.__definitionManager = parser.get_definition_manager()

        # podłoże
        gm = self.__groundManager = parser.get_ground_manager()
        self.__grounds = gm.get_all_grounds()

        nextPosition = 0.0
        for ground in self.__grounds:
            name = ground.get_name()
            defn = self.__definitionManager.get_definition(name)
            if not defn:
                print "Nie znaleziono definicji dla %s" % name
            else:
                animationName = defn.get_animation_name()
#             print "%s    %s  %s" % (name, animationName, nextPosition)
            frame = self.__spriteManager.get_frame(name,animationName,0)
            ground.set_position( (nextPosition,0) )
            groundWidth = frame.width/self.__window_draw_dim[0]
            nextPosition = nextPosition + groundWidth
        
        return True


    def get_background_filenames(self):
        ''' Zwraca listę nazw plików z dostępnymi tłami.'''
        fs = self.__backgroundManager.get_filenames()
        assert len(fs)>0, "Brak plików z tłami."
        return fs

    def __update_entities(self, dt, gameWorld):
        delete_counter = 0                                     # liczba obiektów do usunięcia z początku listy
        for object in self.__levelObjects:
            if object.get_position_x() > self.__creatorPos:    # twórz dopóki obiekty są przed tworzycielem
                break
            delete_counter += 1
            obj = self.__objectFactory.create_object( object.get_name() )  # utwórz obiekt fabryką
            if obj:
                pos = object.get_screen_position()                         # ustaw pola
                coords1,coords3 = self.__window_coords[1],self.__window_coords[3]
                obj.position = multiply_pair(pos,(coords1,coords3))
                gameWorld.add_object( obj )                                # i dodaj od świata
        self.__levelObjects = self.__levelObjects[ delete_counter : ]


    def __update_scenery_objects(self, dt, gameWorld):
        delete_counter = 0                                     # liczba obiektów do usunięcia z początku listy
        for object in self.__sceObjects:
            if object.get_position_x() > self.__creatorPos:    # twórz dopóki obiekty są przed tworzycielem
                break
            delete_counter += 1
            obj = self.__objectFactory.create_object( object.get_name() )   # utwórz obiekt fabryką
            if obj:
                pos = object.get_screen_position()                          # ustaw pola
                coords1,coords3 = self.__window_coords[1],self.__window_coords[3]
                obj.position = multiply_pair(pos,(coords1,coords3))
                gameWorld.add_object( obj )                                 # i dodaj od świata
        self.__sceObjects = self.__sceObjects[ delete_counter : ]


    def __update_grounds(self, dt, gameWorld):
        delete_counter = 0                                     # liczba obiektów do usunięcia z początku listy
        for ground in self.__grounds:
            delete_counter += 1
            obj = self.__objectFactory.create_object( ground.get_name() )
            if obj:
                obj.position = ground.get_position()
#                 print "POS:",obj.position
                gameWorld.add_object( obj )
        self.__grounds = self.__grounds[ delete_counter : ]


    def update(self, dt, gameWorld):
        ''' Aktualizuje menedżer o czas dt udostępniając świat, aby można było dodać obiekty. '''

        # przesuń tworzyciela
        prevCreatorPos=self.__creatorPos
        self.__creatorPos += dt * self.__scrollSpeed * self.__screenResolution

        # dodaj obiekty, na które nadszedł czas
        self.__update_entities( dt, gameWorld )
        self.__update_scenery_objects( dt, gameWorld )
        self.__update_grounds( dt, gameWorld )

        #
        # Trzeba dodać interfejs typu "level_finishing,
        # level_finished, level_starting, level_started", aby
        # gameWorld wiedział kiedy robić przejścia
        #
        # Musi też być metoda next_level, która przechodzi do następnego poziomu
        # 


def multiply_pair( st, nd ):
    return ( st[0]*nd[0], st[1]*nd[1] )

