#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy

from spriteStrategy import SpriteScriptStrategy
from spriteScriptParser import SpriteScriptParser


class GameObjectCreator(object):
    ''' Enkapsulacja algorytmu tworzenia obiektu. Dla każdego istotnie
    różnego obiektu należy utworzyć jedną podklasę tej klasy,
    implementując konkretny algorytm tworzenia obiektu

    Tworzenie oznacza zwrócenie przez metodę create świeżo
    wypieczonego egzemplarza odpowiedniej klasy
    '''

    def __init__(self, spriteManager):
        '''
        objectFactory: Fabryka obiektów
        spriteManager: Zarządca sprite'ów
        '''
        self.spriteManager  = spriteManager # zarządca sprite'ów
        self.spriteName     = None      # nazwa ładowanego sprite'a

        self.parser         = None      # parser plików konfiguracyjnych
        self.spriteStrategy = None      # strategia zarządzania spritem
        self.aiStrategy     = None      # strategia ai nowego obiektu

        self.object         = None      # wynik wypiekania obiektu

    def create(self, spriteName):
        ''' Metoda szablonowa, tworząca obiekt. Należy ją wywołać aby
        stworzyć obiekt
        objName      : Pod jaką nazwą zarejestrować obiekt w fabryce obiektów
        spriteName   : Jakiego sprite'a załadować
        '''

        #
        # FIXME:
        #
        # opis metody sugeruje jeszcze argument objName. Coś go nie widać :-/
        #

        self.spriteName = spriteName
        
        self.parser = SpriteScriptParser( self.spriteName )
        self.parser.parse()
        
        self.create_object()      # implementacja w klasie pochodnej
        
        self.object.set_sprite_name( self.spriteName )
        self.spriteStrategy = SpriteScriptStrategy( self.parser.get_logic_part() )
        self.object.set_sprite_strategy( self.spriteStrategy )
        
        self.create_ai_strategy() # implementacja w klasie pochodnej

        self.object.set_ai_strategy( self.aiStrategy )
        self.spriteManager.load_sprite( self.spriteName, self.parser.get_sprite_part() )
        self.create_related_objects()
        
        return self.object

    #
    # Poniższe metody powinny być CHRONIONE. Należy je w ten sposób
    # traktować.  Jedynym poprawnym ich zastosowaniem jest
    # dostarczenie ich implementacji w podklasach metoda create, która
    # jest publiczna, dba o prawidłowe ich wywoływanie
    #
        
    def create_object(self): abstract
    ''' Implementując tę metodę należy utworzyć obiekt self.object
        np. self.object = PlayerGameObject() '''

    def create_ai_strategy(self): abstract
    ''' Implmeentując tę metodę należy utworzyć pole
    self.aiStrategy. Powinna to być strategia zachowania (AI), która
    ma być przypisana do obiektu.

    przykładowo:
    self.aiStrategy = HeliAIStrategy( self.object, self.spriteStrategy, self.gameWorld )
    '''

    def create_related_objects(self):
        ''' Tworzenie powiązanych obiektów. Np. helikopter powinien
        utworzyć rakiety i pociski, a jeep działko i pociski. Kaczucha
        może chcieć utworzyć części składowe itp.

        Ideą jest swtorzenie wszystkich obiektów potrzebnych do
        funkcjonowania obiektu głównego

        Jeżeli obiekt nie tworzy tego typu obiektów, to nie ma powodu,
        żeby dostarczał tę metodę.
        '''
        pass

    
class GameObject(object):

    def __init__(self):
        self.__spriteName = None         # nazwa sprit'a przypisana do obiektu
        self.__pos = None                # pozycja obiektu (lewy dolny róg). Para (xPos, yPos)
        self.__vel = (0.0, 0.0)          # wektor prędkości. Para (xVel, yVel)
        self.__aiStrategy = None         # strategia wykorzystywana przez obiekt (GameObjectAIStrategy)
        self.__spriteStrategy = None     # strategia zarządzająca stanem animacji (SpriteStrategy)
        self.__destroyed = False         # czy obiekt jest zniszczony i powinien być zdjęty z listy obiektów?


    def display_pad(self):
        ''' Zwraca informację o tym, czy podkładka ma być wyświetlona,
        tzn. czy pod sprite'm ma być wyświetlony jego aabb.'''
        return False
        
    def __set_vel(self, vel): self.__vel = vel
    velocity = property(lambda self: self.__vel,
                        __set_vel)

    
    def __set_pos(self, pos): self.__pos = pos
    def get_pos(self): return self.__pos
    position = property(lambda self: self.__pos,
                        __set_pos)    

    
    def set_sprite_name(self, val): self.__spriteName = val
    spriteName = property(lambda self: self.__spriteName,
                          set_sprite_name)

    
    def set_ai_strategy(self, val): self.__aiStrategy = val
    aiStrategy = property(lambda self: self.__aiStrategy,
                          set_ai_strategy)

    
    def set_sprite_strategy(self,val): self.__spriteStrategy = val
    spriteStrategy = property(lambda self: self.__spriteStrategy,
                              set_sprite_strategy)


    def get_current_animation_name(self):
        if self.__spriteStrategy:
            return self.__spriteStrategy.get_animation_name()
        else:
            print "WARNING: GameObject nie ma spriteStrategy"
            return None

        
    def get_current_frame_num(self):
        if self.__spriteStrategy:
            return self.__spriteStrategy.get_current_frame_num()
        else:
            print "WARNING: GameObject nie ma spriteStrategy"
            return None

        
    def clone(self):
        abstract

        
    def clone_base(self, obj):
        ''' Klonuje część obiektu, która należy do klasy GameObject

        UWAGA: Ta metoda jest chroniona!!! Nie należy do
        interfejsu. Nie używaj poza hierarchią klas GameObject'''
        
        obj.spriteName     = self.spriteName
        obj.position       = self.position
        obj.velocity       = self.velocity
        obj.spriteStrategy = deepcopy(self.spriteStrategy)
        obj.aiStrategy     = deepcopy(self.aiStrategy)
        obj.aiStrategy.set_game_object(obj)
        
        return obj

    
    def hit(self, damage):
        ''' Obsługa trafienia z siłą 'damage' '''
        abstract

        
    def destroy(self):
        self.__destroyed = True

    
    def isDestroyed(self):
        return self.__destroyed

        
    def update(self, dt):
        # update obiektu
        (xPos, yPos) = self.position
        (xVel, yVel) = self.velocity
        xPos += xVel * dt
        yPos += yVel * dt
        self.position = (xPos, yPos)
        
        # update logiki obiektu
        if self.__aiStrategy:
            self.__aiStrategy.update( dt )
        else:
            print 'Error: ups, no aiStrategy assigned.', self.__class__

        # update logiki sprite'a
        if self.__spriteStrategy:
            self.__spriteStrategy.update( dt )
        else:
            print 'Error: ups, no scriptStrategy assigned.', self.__class__


    def collide(self, object, depth = 0):
        ''' Metoda obsługuje kolizję z object.

        object: Obiekt, z którym jest sprawdzana kolizja
        
        depth: 0 - metoda wywołana przez gameWorld, każda
        większa wartość oznacza liczbę razy wywołań collide w
        collide. Obiekt obsługując kolizję może wywołać colilde
        drugiego obiektu. Powinien wtedy zwiększyć głębokość o 1

        
        collide innego obiektu (True), czy przez zarządcę (False)
        '''
        if depth > 1: return
        object.collide(self, depth + 1)


class GameObjectEnemy(GameObject):
    def __init__(self):
        GameObject.__init__(self)
