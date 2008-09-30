#!/usr/bin/python
# -*- coding: utf-8 -*-

from collisionManager import CollisionManager
from spriteManager import SpriteManager
from gameObject import GameObject
from pyglet.gl import *


class GameWorld(object):

    def __init__(self):
        # lista obiektów w świecie
        self.__objects = []

        # menadżer kolizji
        self.__collisionManager = CollisionManager()

        # menadżer sprite'ów
        self.__spriteManager = SpriteManager()

    collisionManager = property( lambda self: self.__collisionManager )
    spriteManager = property( lambda self: self.__spriteManager )


    def add_object(self, gameobject):
        ''' Dodaje obiekt do świata. Sprawdza typ dodawanego obiektu. '''
        try: isinstance(gameobject, GameObject),
        except TypeError, msg: print msg, "Obiekt nie jest typu GameObject."

        self.__objects.append( gameobject )
        self.collisionManager.add_object( gameobject )


    def remove_object(self, gameobject):
        ''' Usuwa wszystkie wystąpienia obiektu w świecie. '''
        for i in range(self.__objects.count(gameobject)):
            self.__objects.remove( gameobject )
            self.collisionManager.remove_object( gameobject )


    def update(self, dt):
        ''' Aktualizuje obiekty ze świata. '''
        self.check_collisions()
        for obj in self.__objects:
            obj.update( dt )


    def __draw_rect(self, texCoords, frameRect, scrPos):
        ''' Rysuje czworokąt texCoords z aktualnej tekstury na ekranie w miejscu
        scrPos. Pozycja i wymiary czworokąta opisane są przez frameRect (x-lewo,y-dół,x-prawo,y-góra). '''
        if not len(texCoords)==4:
            print "Error: __draw_rect, zła ilość współrzędnych w texCoords (%d zamiast %d)"%(len(texCoords),4)
            return
        if not len(frameRect)==4:
            print "Error: __draw_rect, zła ilość współrzędnych w frameRect (%d zamiast %d)"%(len(frameRect),4)
            return
        if not len(scrPos)==3:
            print "Error: __draw_rect, zła ilość współrzędnych w scrPos (%d zamiast %d)"%(len(scrPos),3)
            return
        # ustaw OpenGL
        glColor4f( 1, 1, 1, 1 )
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
        # narysuj oteksturowany czworokąt
        glTranslatef( *scrPos )
        left,bottom,right,top = texCoords
        tc = ( (left,bottom), (right,bottom), (right,top), (left,top) )
        left,bottom,right,top = frameRect
        vs = ( (left,bottom), (right,bottom), (right, top), (left, top) )
        glBegin( GL_QUADS )
        for t,v in zip(tc,vs):
            glTexCoord2f( *t )
            glVertex2f( *v )
        glEnd()


    def draw(self):
        ''' Rysuje wszystkie obiekty w świecie. '''
        glClearColor( 1, .5, 0, 0 )
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        for obj in self.__objects:
            sname = obj.spriteName
            #
            # FIXME
            # pobranie animName i frameNum z jakiegos menadżera stanów
            #
            animName = ''
            frameNum = obj.spriteStrategy.curFrameNum

            frame = self.spriteManager.get_frame( sname, animName, frameNum )
            glPushMatrix()
            glEnable( frame.texture.target )
            glBindTexture( frame.texture.target, frame.texture.id )
            self.__draw_rect( frame.rect, (0, 0, .5, .5), (0,0,0) )
            glPopMatrix()


    def check_collisions(self):
        collPairs = self.collisionManager.get_colliding_objects()
