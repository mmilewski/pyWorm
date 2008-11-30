#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.dom.minidom as xmlDom

'''
Moduł parsujący zawartość pliku opisującego poziom.
'''

# DEBUG version, wypisuje dużo tekstu.


# need help with XML? see http://www.python.org/doc/2.5.2/lib/node217.html

class LevelAction:
    ''' Klasa bazowa opizująca akcję w poziomie.'''

    def perform(self):abstract
        ''' Wykonuje akcję. metoda musi zostać przeciążona w klasie pochodnej.'''
        pass

    def get_next_perform_time(self):abstract
        '''Zwraca czas kiedy powinno nastąpić następne wykonanie akcji.'''
        pass

class CreateObjectLevelAction(LevelAction):
    ''' Klasa akcji. Odpowiada z tworzenie obiekt w poziomie.'''

    def perform(self):
        print "tworzenie obiektu"

    def get_next_perform_time(self):
        return -1;

class StopScrollingLevelAction(LevelAction):
    ''' Klasa akcji. Odpowiada za zatrzymanie przesuwania się poziomu. Np. z powodu bossa.'''

    def perform(self):
        print "zatrzymywanie scrollowania"

    def get_next_perform_time(self):
        return -1;

        
class LevelActionManager:
    ''' Klasa menedżera odpowiada za zarządzaniem akcjami w poziomie.'''
    def __init__(self, actions=[]):
        ''' Inicjuje menedżera podaną listą akcji. '''
        self.__actions=actions;
        
    def perform_up_to(self, msTime=-1):
        ''' Wyzwala wszystkie akcje, które powinny zostać wykonane przed czasem msTime.
        Jeśli msTime=-1, to zostaną uruchomione wszystkie akcje (oczywiście najpierw najstarsze.'''
        pass
        

class LevelParser:
    '''Klasa odczytująca poziom z pliku.'''

    def __init__(self, filename):
        self.__levelAuthor="Gal Anonim"        # domyślne wartości
        self.__levelName="[no level name]"

        print 'Loading level from `%s`...' % filename
        data = xmlDom.parse(filename)
        if not data.hasChildNodes():
            print 'FAILED. Nie znalezono dzieci dla pierwszego elementu.'
            return

        #
        # TODO
        # sprawdzenie poprawności przez xml.sax
        #
        
        lvl = data.childNodes[0]
        if not lvl.nodeName=='level':
            print 'Nieprawidłowy pierwszy tag, oczekiwano `level`'
            return

        # wczytaj dane dotyczące poziomu (nagłówek, akcje, tło, definicje,...)
        for node in lvl.childNodes:
            if node.nodeType==data.ELEMENT_NODE:
                if node.localName=='header': self.__parse_header(node)
                if node.localName=='ground': self.__parse_ground(node)
                if node.localName=='actions': self.__parse_actions(node)
                if node.localName=='background': self.__parse_background(node)
                if node.localName=='definitions': self.__parse_definitions(node)

    def __parse_header(self, node):
        '''Przetwarza nagłówek.'''
        print 'parsing header'
        # wyłuskaj autora
        authorList = node.getElementsByTagName('author')
        self.__levelAuthor = authorList[0].childNodes[0].data if len(authorList)>0 else self.__levelAuthor

        # wyłuskaj nazę poziomu
        namesList = node.getElementsByTagName('name')
        self.__levelName = namesList[0].childNodes[0].data if len(namesList)>0 else self.__levelName

        print "\tauthor = `%s`, \n\tlevelName = `%s`" % (self.__levelAuthor, self.__levelName)

    def __parse_definitions(self, node):
        '''Przetwarza definicje.'''
        print 'parsing definitions'
        for defn in node.getElementsByTagName('definition'):
            for sprite in defn.getElementsByTagName('sprite'):
                 fname = sprite.getAttribute('filename') if sprite.hasAttribute('filename') else ''
                 aname = sprite.getAttribute('animation') if sprite.hasAttribute('animation') else ''
                 print "\tsprite \n\t\tfilename=`%s` \n\t\tanimation=`%s`" % (fname,aname)
                    

    def __parse_actions(self, node):
        '''Przetwarza akcje.'''
        print 'parsing actions'
        for cobj in node.getElementsByTagName('createObject'):
            print "\tcreateObject"
            for time in cobj.getElementsByTagName('time'):
                 s = time.getAttribute('s') if time.hasAttribute('s') else 0
                 ms = time.getAttribute('ms') if time.hasAttribute('ms') else 0
                 print "\t\ttime with s=%d, ms=%d" % (int(s), int(ms))
            for pos in cobj.getElementsByTagName('position'):
                 x = pos.getAttribute('x') if pos.hasAttribute('x') else 0
                 y = pos.getAttribute('y') if pos.hasAttribute('y') else 0
                 print "\t\tposition with x=%d , y=%d" % (int(x), int(y))
        for stScroll in node.getElementsByTagName('stopScrolling'):
            print "\tstopScrolling"
            for time in stScroll.getElementsByTagName('time'):
                 s = time.getAttribute('s') if time.hasAttribute('s') else 0
                 ms = time.getAttribute('ms') if time.hasAttribute('ms') else 0
                 print "\t\ttime with s=%d, ms=%d" % (int(s), int(ms))

    def __parse_ground(self, node):
        '''Przetwarza dane związane z podłożem.'''
        print 'parsing ground'
        for part in node.getElementsByTagName('part'):
            print "\tpart"
            if part.hasAttribute('name'):
                name=part.getAttribute('name')
                print "\t\tname = %s" % name
            if part.hasAttribute('repeat'):
                repeat=part.getAttribute('repeat')
                print "\t\trepeat = %s" % repeat
            if part.hasAttribute('joinWithNext'):
                joinWithNext=part.getAttribute('joinWithNext')
                print "\t\tjoinWithNext = %s" % joinWithNext
            if part.hasAttribute('useJoin'):
                useJoin=part.getAttribute('useJoin')
                print "\t\tuseJoin = %s" % useJoin

    def __parse_background(self, node):
        '''Przetwarza dane związane z tłem.'''
        print 'parsing background'
        for part in node.getElementsByTagName('part'):
            print "\tpart"
            if part.hasAttribute('name'):
                name=part.getAttribute('name')
                print "\t\tname = %s" % name
            if part.hasAttribute('repeat'):
                repeat=part.getAttribute('repeat')
                print "\t\trepeat = %s" % repeat

    def get_level_author(self):
        '''Zwraca autora poziomu.'''
        return self.__levelAuthor

    def get_level_name(self):
        '''Zwraca nazwę/tytuł poziomu.'''
        return self.__levelName

    
