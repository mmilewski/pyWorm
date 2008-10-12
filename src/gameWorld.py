#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet.gl import *

import sys
sys.path.append("game_objects/") # konieczne do korzystania z game_objectów

# zarządcy
from collisionManager import CollisionManager
from levelManager import LevelManager
from spriteManager import SpriteManager

# obiekty gry
from supportedObjects import add_supported_objects_to_factory
from gameObjectFactory import GameObjectFactory
from gameObject import GameObject
from playerGameObject import PlayerGameObject, PlayerHeliAIStrategy, PlayerHeliCreator

# sprite'y
from spriteStrategy import SpriteScriptStrategy
from spriteScriptParser import SpriteScriptParser


class GameWorld(object):

    def __init__(self, theApp):
        ''' theApp: refernecja do obiektu aplikacji. Potrzebne przy dodawaniu obiektu nasłuchującego wejścia '''

        self.__theApp = theApp                                              # obiekt zarządzający aplikacją
        self.__objects = []                                                 # lista obiektów w świecie
        
        self.__collisionManager = CollisionManager()                        # menadżer kolizji
        self.__spriteManager    = SpriteManager()                           # menadżer sprite'ów
        self.__objectFactory    = self.__create_object_factory()            # fabryka obiektów
        self.__levelManager     = LevelManager(self.__objectFactory)        # menadżer poziomów
        
        self.__levelManager.load_level("test_level")

        # Dodaj obiekt helikoptera i jeepa do gry
        self.add_object(self.__create_heli())
        

    def add_object(self, gameobject):
        ''' Dodaje obiekt do świata. Sprawdza typ dodawanego obiektu. '''
        try: isinstance(gameobject, GameObject),
        except TypeError, msg: print msg, "Dodawany obiekt nie jest typu GameObject."

        self.__objects.append( gameobject )
        self.__collisionManager.add_object( gameobject )


    def remove_object(self, gameobject):
        ''' Usuwa wszystkie wystąpienia obiektu w świecie. '''
        for i in range(self.__objects.count(gameobject)):
            self.__objects.remove( gameobject )
            self.collisionManager.remove_object( gameobject )


    def create_object(self, objName):
        ''' Tworzy obiekt o zadanej nazwie korzystając z fabryki
        obiektów.  '''
        return self.__objectFactory.create_object( objName )
        
            
    def update(self, dt):
        ''' Aktualizuje obiekty ze świata. '''
        self.__objects = filter(lambda o: not o.isDestroyed() , self.__objects)
        
        self.check_collisions()
        for obj in self.__objects:
            obj.update( dt )

            
    def draw(self):
        ''' Rysuje wszystkie obiekty w świecie. '''
        glClearColor( 0, 0, 0, 0 )
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();

        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
        
        for obj in self.__objects:
            spriteName  = obj.spriteName
            animName    = obj.get_current_animation_name()
            frameNum    = obj.get_current_frame_num()
            frame     = self.__spriteManager.get_frame( spriteName, animName, frameNum )
            
            (tc,vs)   = self.__compute_tex_vertex_coords( obj, frame )
            textureId = frame.textureId
            
            glPushMatrix()
            glEnable( GL_TEXTURE_2D )
            glBindTexture( GL_TEXTURE_2D, textureId )
            
            glBegin( GL_QUADS )
            for t,v in zip(tc,vs):
                glTexCoord2f( *t )
                glVertex2f( *v )
            glEnd()

            glDisable( GL_TEXTURE_2D )
            glPopMatrix()


    def __compute_tex_vertex_coords(self, obj, frame):
        ''' zwraca parę (współrzędne tekstury, współrzędne wierzchołka) dla obiektu `obj` '''

        tex_left, tex_bottom, tex_right, tex_top = frame.rect
        winWidth, winHeight = self.__theApp.get_window_dim()
        
        vertex_left, vertex_bottom = obj.position
        vertex_right = vertex_left + frame.width / winWidth
        vertex_top = vertex_bottom - frame.height / winHeight
        
        tc = ( (tex_left, tex_bottom), (tex_right, tex_bottom), (tex_right, tex_top), (tex_left, tex_top) )
        vs = ( (vertex_left, vertex_bottom), (vertex_right, vertex_bottom), (vertex_right, vertex_top), (vertex_left, vertex_top) )

        return (tc,vs)
    

    def check_collisions(self):
        ''' Pobiera pary kolidujących obiektów i nakazuje obsługę któremuś z nich. '''
        collPairs = self.__collisionManager.get_colliding_objects()
        for a,b in collPairs:
            if a != b:
                a.collide(b)

                
    def __create_object_factory(self):
        ''' Tworzy instancję fabryki obiektów '''
        objFactory = GameObjectFactory()
        add_supported_objects_to_factory(objFactory)
        return objFactory


    def __create_heli(self):
        creator = PlayerHeliCreator( self.__theApp, self, self.__spriteManager, self.__objectFactory )
        heli = creator.create( 'heli' )
        heli.position = (0.1, 0.7)
        
        return heli
