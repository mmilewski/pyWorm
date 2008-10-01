#!/usr/bin/python
# -*- coding: utf-8 -*-

from goHeli import HeliGO
from goJeep import JeepGO


class LevelManager(object):

    def __init__(self):
        pass


    def load_level(self, levelName):
        print 'Ładowanie poziomu `%s`' % levelName
        name = str(levelName)
        list = ['heli','jeep']
        if name=='1':
            list.extern( ['ground_cannon'] )
        elif name=='krowi poziom':
            print "GL & HF"
        else:
            print "Tworzenie poziomu `%s` NIE powiodło się. Nieznana nazwa." % levelName
            return
        self.__load_game_objects( list )


    def __load_game_objects(self, objectsNameList):
        ''' Tworzy obiekty na podstawie ich nazw.
        Zwraca fabrykę zdolną tworzyć wskazane w objectsNameList obiekty. '''
        fatory = GameObjectFactory()
        for objName in objectsNameList:
            obj = self.__name2object(objName)
            if obj:
                factor.register_game_object()
        return factory


    def __name2object(self, objectName):
        d = { 'heli': HeliGO(),
              'jeep': JeepGO()    }
        if d.has_key(objectName): return d[objectName]
        else:
            print "Brak obiektu odpowiadającego nazwie `%s`" % objectName
            return None
