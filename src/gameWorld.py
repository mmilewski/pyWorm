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
from playerGameObject import PlayerGameObject
from playerHeli import PlayerHeliAIStrategy, PlayerHeliCreator

# sprite'y
from spriteStrategy import SpriteScriptStrategy
from spriteScriptParser import SpriteScriptParser
from pyglet import image

# dodatkowe
from math import sin, cos


class GameWorld(object):

    def __init__(self, theApp):
        ''' theApp: refernecja do obiektu aplikacji. Potrzebne przy dodawaniu obiektu nasłuchującego wejścia '''

        self.__theApp = theApp                                              # obiekt zarządzający aplikacją
        self.__objects = []                                                 # lista obiektów w świecie
        
        self.__spriteManager    = SpriteManager()                           # menadżer sprite'ów
        self.__collisionManager = CollisionManager(self.__spriteManager)    # menadżer kolizji
        self.__objectFactory    = self.__create_object_factory(self.__spriteManager) # fabryka obiektów
        self.__levelManager     = LevelManager(self.__objectFactory)        # menadżer poziomów
        
        self.__levelManager.load_level("demo_level")

        # utwórz teksturę, do której będzie renderowany obraz
        #
        # FIXME: rozmiar tekstury powinna definiować stała
        #
        img = image.create( 512, 512 )
        self.__renderTexture = img.get_texture()
        
        # Dodaj obiekt helikoptera i jeepa do gry
        #
        # FIXME: jeep?
        #
        self.add_object( self.__create_heli() )



#         #
#         # FIXME: Do usunięcia (powinno być obsługiwane przez zarządcę poziomu
#         # 
#         obj = self.__objectFactory.create_object( 'helicopter1' )
#         obj.position = (0.7, 0.1)
#         self.add_object(obj)

#         obj = self.__objectFactory.create_object( 'helicopter1' )
#         obj.position = (0.7, 0.3)
#         self.add_object(obj)

#         obj = self.__objectFactory.create_object( 'helicopter1' )
#         obj.position = (0.7, 0.5)
#         self.add_object(obj)

#         obj = self.__objectFactory.create_object( 'helicopter1' )
#         obj.position = (0.45, 0.3)
#         self.add_object(obj)

        self.__swingAngle = 0.0   # kołysanie się wyrenderowanej tekstury

        
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
        
        # progres animacji
        self.__swingAngle += dt*100

        # aktualizacja menedżera poziomu (np. stworzenie nowych jednostek)
        self.__levelManager.update( dt, self )

        # odfiltruj obiekty, które są zniszczone
        for o in self.__objects:
            if o.isDestroyed():
                self.__collisionManager.remove_object(o)
        self.__objects = filter(lambda o: not o.isDestroyed() , self.__objects)

        # sprawdź kolizje
        self.check_collisions()

        # aktualizuj stan obiektów
        for obj in self.__objects:
            obj.update( dt )


    def __draw_object( self, obj ):
        ''' Rysuje obiekt przekazany jako argument. '''
        glPushMatrix()

        # przygotuj mieszanie kolorów
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

        # zbierz informacje o reprezentacji obiektu
        spriteName  = obj.spriteName
        animName    = obj.get_current_animation_name()
        frameNum    = obj.get_current_frame_num()
        frame     = self.__spriteManager.get_frame( spriteName, animName, frameNum )
        (tc,vs)   = self.__compute_tex_vertex_coords( obj, frame )
        textureId = frame.textureId

        # narysuj tło pod sprite'em (do celów testowych)
        if( obj.display_pad() ):
            glDisable( GL_TEXTURE_2D )
            glColor3f( .3, .3, .4 )     # ew. kolor może być skądś pobierany
            glBegin( GL_QUADS )
            for v in vs:
                glVertex2f( *v )
            glEnd()

        # wyświetlenie czworokąta/sprite'a
        glEnable( GL_TEXTURE_2D )
        assert glIsTexture( textureId ), "Próba narysowania czegoś, co nie jest teksturą, jest %s" % type(textureId)
        glBindTexture( GL_TEXTURE_2D, textureId )
        glBegin( GL_QUADS )
        for t,v in zip(tc,vs):
            glTexCoord2f( *t )
            glVertex2f( *v )
        glEnd()
        glDisable( GL_TEXTURE_2D )

        glPopMatrix()


    def draw(self):
        ''' Rysuje wszystkie obiekty w świecie. '''
        glClearColor( 0.5, 0.5, 0.5, 0.5 )
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()

        # zmień viewport, będziemy renderować do tekstury
        #
        # FIXME: rozmiar tekstury powinna definiować jakaś stała
        #
        glViewport( 0, 0, 512, 512 )

        # narysuj wszystkie obiekty
        for obj in self.__objects:
            self.__draw_object( obj )

        # zapisz bufor do tekstury
        assert glIsTexture( self.__renderTexture.id ),"Próba narysowania czegoś, co nie jest teksturą, %s" % type(self.__renderTexture.id)
        glBindTexture( GL_TEXTURE_2D, self.__renderTexture.id )
        glCopyTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, 0, 0, 512, 512, 0)
#         glCopyTexSubImage2D( GL_TEXTURE_2D, 0, 0, 0, 0, 0, 512, 512)

        # przywróć viewport, wyczyść bufor i narysuj czworokąt z zapisaną teksturą
        winSize = map( lambda x:int(x), self.__theApp.get_window_dim() )
        glViewport( 0, 0, winSize[0], winSize[1] )
        glClearColor( 0.5, 0.5, 0.5, 0.5 )
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glEnable( GL_TEXTURE_2D )
        glColor3f( .5, 1, 1 )

        # zrób galarete :D
        glScalef( .9+sin(self.__swingAngle)/100, .9+cos(self.__swingAngle)/80, 1 )

        coords = self.__theApp.get_window_coords()   # czworokąt zajmujący cały ekran
        x0,x1,y0,y1 = coords[0], coords[1], coords[2], coords[3]
        tc = [ (  0,  0), (  1,  0), (  1,  1), (  0,  1) ]
        vs = [ ( x0, y0), ( x1, y0), ( x1, y1), ( x0, y1) ]
        glBegin( GL_QUADS )
        for t,v in zip(tc,vs):
            glTexCoord2f( *t )
            glVertex2f( *v )
        glEnd()

        # zrzuć wszystko
        glFlush()


    def __compute_tex_vertex_coords(self, obj, frame):
        ''' Zwraca parę (współrzędne tekstury, współrzędne wierzchołka) dla obiektu `obj` '''

        tex_left, tex_bottom, tex_right, tex_top = frame.rect
        winWidth, winHeight = self.__theApp.get_window_dim()
        
        vertex_left, vertex_bottom = obj.position
        vertex_right = vertex_left + frame.width / winWidth
        vertex_top = vertex_bottom + frame.height / winHeight
        
        tc = ( (tex_left, tex_bottom), (tex_right, tex_bottom), (tex_right, tex_top), (tex_left, tex_top) )
        vs = ( (vertex_left, vertex_bottom), (vertex_right, vertex_bottom), (vertex_right, vertex_top), (vertex_left, vertex_top) )

        return (tc,vs)
    

    def check_collisions(self):
        ''' Pobiera pary kolidujących obiektów i nakazuje obsługę któremuś z nich. '''
        collPairs = self.__collisionManager.get_colliding_objects()
        for a,b in collPairs:
            if a != b:
                a.collide(b)

                
    def __create_object_factory(self, spriteManager):
        ''' Tworzy instancję fabryki obiektów '''
        objFactory = GameObjectFactory()
        add_supported_objects_to_factory(objFactory, spriteManager)
        return objFactory


    def __create_heli(self):
        ''' Tworzy helikopter gracza. '''
        creator = PlayerHeliCreator( self.__theApp, self, self.__spriteManager, self.__objectFactory )
        heli = creator.create( 'heli' )
        heli.position = (0.1, 0.5)
        return heli
