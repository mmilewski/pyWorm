#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

from inputManager import InputObserver

from aiStrategy import AIStrategy
from gameObject import GameObject, GameObjectCreator

from rocketGameObject import SimpleRocketCreator


class PlayerGameObject(GameObject):
    
    def __init__(self):
        GameObject.__init__(self)
    
    def clone(self):
        raise "Obiektu gracza nie można klonować"

    def collide(self, object):
        pass


class PlayerHeliAIStrategy(AIStrategy, InputObserver):

    def __init__(self, gameObject, spriteStrategy, gameWorld):
        self.__actionFire     = False            # czy gracz strzela
        self.__actionAutofire = False            # czy gracz cały czas ma strzelać
        self.__coolDown       = 0.0              # ile trzeba odczekaż aby móc znów wystrzelić
        self.__coolDownTime   = 0.2              # czas na jaki jest ustawiane __coolDown po każdym strzale
        
        self.__gameObject     = gameObject       # refrencja do obiektu, którym strategia zarządza
        self.__spriteStrategy = spriteStrategy   # referencja do strategii sprite'a obiektu gameObject
        self.__gameWorld      = gameWorld

        self.__spriteStrategy.set_animation('default')

        
    def update(self, dt):
        # obsłuż broń
        self.__coolDown -= dt
        if self.__coolDown < 0.0:
            self.__coolDown = 0.0
        
        if self.__actionAutofire or self.__actionFire:
            if self.__coolDown <= 0.0:
                self.__fire()
                self.__coolDown = self.__coolDownTime
        
                
    def __fire(self):
        rocket = self.__gameWorld.create_object( 'heli_rocket' )
        (xPos, yPos) = self.__gameObject.position
        (xVel, yVel) = self.__gameObject.velocity
        xPos += 0.15
        yPos -= 0.10
        rocket.position = (xPos, yPos)
        rocket.velocity = (0.8, 0.0)
        self.__gameWorld.add_object( rocket )
        
        
    def notify_input(self, subject):
        xVel, yVel = 0.0, 0.0

        # obsługa animacji
        if subject.get_key_state('left'):
            self.__spriteStrategy.set_animation('pochyla sie tyl')

        if subject.get_key_state('right'):
            self.__spriteStrategy.set_animation('pochyla sie przod')

        if not (subject.get_key_state('left') or subject.get_key_state('right')):
            self.__spriteStrategy.set_animation('default')
                    
        # obsługa kierunku lotu
        if subject.get_key_state('up'): yVel =  0.35
        if subject.get_key_state('down'): yVel = -0.35
        if subject.get_key_state('right'): xVel =  0.35
        if subject.get_key_state('left'): xVel = -0.25
        self.__gameObject.velocity  = (xVel, yVel)
        
        # obsługa broni
        if subject.get_key_state('enter'):
            self.__actionAutofire = not self.__actionAutofire
        
        self.__actionFire = False;
        if subject.get_key_state('rctrl'): self.__actionFire = True


class PlayerHeliCreator(GameObjectCreator):
    def __init__(self, theApp, gameWorld, spriteManager, objectFactory):
        GameObjectCreator.__init__(self, spriteManager)
        self.__theApp    = theApp
        self.__gameWorld = gameWorld
        self.__objectFactory = objectFactory

    def create_object(self):
        self.object = PlayerGameObject()

    def create_ai_strategy(self):
        self.aiStrategy = PlayerHeliAIStrategy( self.object, self.spriteStrategy, self.__gameWorld )
        self.__theApp.register_input_observer( self.aiStrategy )        
        
    def create_related_objects(self):
        creator = SimpleRocketCreator( self.spriteManager )
        self.__objectFactory.register_game_object( creator.create( 'heli_rocket' ), 'heli_rocket' )
