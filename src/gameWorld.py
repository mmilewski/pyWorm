#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet.gl import *

import sys
sys.path.append("game_objects/") # konieczne do korzystania z game_objectów

# zarządcy
from collisionManager import CollisionManager
from levelManager import LevelManager
from spriteManager import SpriteManager
from backgroundManager import BackgroundManager

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

# pomocnicze
from render_toolkit import draw_textured_quad, compute_tex_vertex_coords
import const
import config

from groundObject import GroundObject
from sceneryObject import SceneryObject


class GameWorld(object):

    def __init__(self, theApp):
        ''' theApp: refernecja do obiektu aplikacji. Potrzebne przy dodawaniu obiektu nasłuchującego wejścia. '''

        self.__theApp = theApp                                              # obiekt zarządzający aplikacją
        self.__objects = []                                                 # lista obiektów w świecie

        self.__spriteManager     = SpriteManager()                           # menadżer sprite'ów
        self.__collisionManager  = CollisionManager(self.__spriteManager)    # menadżer kolizji
        self.__objectFactory     = self.__create_object_factory(self.__spriteManager) # fabryka obiektów
        self.__levelManager      = LevelManager(self.__objectFactory,self.__spriteManager)  # menadżer poziomów
        self.__backgroundManager = BackgroundManager( levelManager = self.__levelManager )
        self.__backgroundManager.set_window_coords( self.__theApp.get_window_coords() )
        self.__backgroundManager.set_window_draw_dim( self.__theApp.get_window_draw_dim() )
        self.__levelManager.set_window_coords( self.__theApp.get_window_coords() )
        self.__levelManager.set_window_draw_dim( self.__theApp.get_window_draw_dim() )

        if not self.__levelManager.load_level("demo_level"):
            assert True, "Tworzenie świata nie powiodło się. Nie można wczytać poziomu."

        const.renderTextureSize = (512,256)                # rozmiary tekstury, do której będziemy renderować
        self.__renderTexture = image.create( *const.renderTextureSize ).get_texture()

        # Dodaj obiekt helikoptera i jeepa do gry
        #
        # FIXME: jeep?
        #
        self.add_object( self.__create_heli() )


    def add_object(self, gameObject):
        ''' Dodaje obiekt do świata. Sprawdza typ dodawanego obiektu. '''
        try: isinstance(gameObject, GameObject),
        except TypeError, msg: print msg, "Dodawany obiekt nie jest typu GameObject."

        self.__objects.append( gameObject )
        self.__collisionManager.add_object( gameObject )


    def remove_object(self, gameObject):
        ''' Usuwa wszystkie wystąpienia obiektu w świecie. '''
        for i in range(self.__objects.count(gameObject)):
            self.__objects.remove( gameObject )
            self.collisionManager.remove_object( gameObject )

    def create_object(self, objName):
        ''' Tworzy obiekt o zadanej nazwie korzystając z fabryki obiektów. '''
        return self.__objectFactory.create_object( objName )


    def get_background_manager(self):
        assert self.__backgroundManager, "Obiekt menedżera tła nie istnieje."
        return self.__backgroundManager


    def update(self, dt):
        ''' Aktualizuje obiekty ze świata. '''

        # aktualizacja menedżera poziomu (np. stworzenie nowych jednostek)
        self.__levelManager.update( dt, self )

        # usuń obiekty, które są za lewą krawędzią planszy
        for obj in self.__objects:
            animName    = obj.get_current_animation_name()
            frame       = self.__spriteManager.get_frame( obj.spriteName, animName, 0 )
            (ww,wh)     = self.__theApp.get_window_draw_dim()
            objectWidth = frame.width / float(ww)
            if obj.position[0]+objectWidth < -0.5:
                print "DELETED:",obj.spriteName
                obj.destroy()

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

        # aktualizuj tło
        self.get_background_manager().update( dt )


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
        (ww,wh)   = self.__theApp.get_window_draw_dim()
        (tc,vs)   = compute_tex_vertex_coords( obj, frame, ww, wh )
        textureId = frame.textureId

        # narysuj tło pod sprite'em (do celów testowych)
        if( obj.display_pad() ):
            glDisable( GL_TEXTURE_2D )
            glColor3f( .3, .3, .4 )     # ew. kolor może być skądś pobierany
            glBegin( GL_QUADS )
            for v in vs:
                glVertex2f( *v )
            glEnd()

        # narysuj sprite'a
        draw_textured_quad( tc, vs, textureId )
        glColor3f( 1, 1, 1 )

        glPopMatrix()


    def draw(self):
        ''' Rysuje wszystkie obiekty w świecie. '''
        glClearColor( 0.4, 0.4, 0.4, 0.5 )
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()

        # zmień viewport, będziemy renderować do tekstury
        if config.IS_RENDER_TO_TEXTURE:
            tw,th = const.renderTextureSize
            glViewport( 0, 0, tw, th )

        glTranslatef( 0, 0, -10 )

        # narysuj tło
        self.get_background_manager().draw_background()

        # narysuj scenerię
        glTranslatef( 0, 0, 1 )
        for obj in filter(lambda o:isinstance(o,SceneryObject),self.__objects):
            self.__draw_object( obj )

        # narysuj jednostki, etc.
        glTranslatef( 0, 0, 1 )
        for obj in self.__objects:
            if not (isinstance(obj,SceneryObject) or isinstance(obj,GroundObject)):
                self.__draw_object( obj )

        # narysuj podłoże
        glTranslatef( 0, 0, 1 )
        for obj in filter(lambda o:isinstance(o,GroundObject) and o.position[0]<1.1,self.__objects):
            self.__draw_object( obj )

        # zapisz bufor do tekstury
        if config.IS_RENDER_TO_TEXTURE:
            assert glIsTexture( self.__renderTexture.id ), "Próba narysowania czegoś, co nie jest teksturą"
            glBindTexture( GL_TEXTURE_2D, self.__renderTexture.id )
            glCopyTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, 0, 0, tw, th, 0 )
#             glCopyTexSubImage2D( GL_TEXTURE_2D, 0, 0, 0, 0, 0, tw, th )

        # przywróć viewport, wyczyść bufor i narysuj czworokąt z zapisaną teksturą
        winSize = map( lambda x:int(x), self.__theApp.get_window_dim() )
        glViewport( 0, 0, winSize[0], winSize[1] )
        if config.IS_RENDER_TO_TEXTURE:
            glClearColor( 0.5, 0.5, 0.5, 0.5 )
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glEnable( GL_TEXTURE_2D )
            glColor3f( 1, 1, 1 )

            # renderuj czworokąt na cały ekran
            coords = self.__theApp.get_window_coords()
            x0,x1,y0,y1 = coords[0], coords[1], coords[2], coords[3]
            tc = [ (  0,  0), (  1,  0), (  1,  1), (  0,  1) ]
            vs = [ ( x0, y0), ( x1, y0), ( x1, y1), ( x0, y1) ]
            draw_textured_quad( tc, vs, self.__renderTexture.id )

        # zrzuć wszystko
        glFlush()
        

    def check_collisions(self):
        ''' Pobiera pary kolidujących obiektów i nakazuje obsługę któremuś z nich. '''

        collPairs = self.__collisionManager.get_colliding_objects()
        for a,b in collPairs:
            if a != b:
                a.collide(b)


    def __create_object_factory(self, spriteManager):
        ''' Tworzy instancję fabryki obiektów. '''

        objFactory = GameObjectFactory()
        add_supported_objects_to_factory(objFactory, spriteManager)
        return objFactory


    def __create_heli(self):
        ''' Tworzy helikopter gracza. '''

        creator = PlayerHeliCreator( self.__theApp, self, self.__spriteManager, self.__objectFactory )
        heli = creator.create( 'heli' )
        heli.position = (0.1, 0.5)
        return heli
