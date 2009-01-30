#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.dom.minidom as xmlDom

'''
Moduł parsujący zawartość pliku opisującego poziom.
'''

# DEBUG version, wypisuje dużo tekstu.


# need help with XML? see http://www.python.org/doc/2.5.2/lib/node217.html


def pos_cmp(action1, action2):
    ''' Komparator dwóch akcji, porządkuje wg czasu występowania. Wcześniejscze najpierw.'''
    if action1.get_position_x() < action2.get_position_x(): return -1
    if action1.get_position_x() > action2.get_position_x(): return 1
    return 0

### AKCJE ###

class LevelAction:
    ''' Klasa bazowa opisująca akcję w poziomie.'''

    def perform(self):
        ''' Wykonuje akcję. metoda musi zostać przeciążona w klasie pochodnej.'''
        abstract

    def get_position_x(self):
        ''' Zwraca współrzędną x akcji. Akcje są sortowane względem tej wartości (najpierw mniejsze).'''
        abstract

class StopScrollingLevelAction(LevelAction):
    ''' Klasa akcji. Odpowiada za zatrzymanie przesuwania się poziomu. Np. z powodu bossa.'''

    def __init__(self, pos):
        assert pos==float(pos), "argument pos musi byc skalarem typu float a nie %s" % type(pos)
        self.__position = float(pos)

    def perform(self):
        print "zatrzymywanie scrollowania na pozycji", self.get_position_x()

    def get_position_x(self):
        return self.__position


class LevelActionManager:
    ''' Klasa menedżera akcji odpowiada za zarządzaniem akcjami w poziomie.'''

    def __init__(self, actions):
        ''' Inicjuje menedżer podaną listą akcji. '''
        self.__actions = actions
        self.__sort_actions()

    def __sort_actions(self):
        ''' Sortuje listę akcji według kolejności występowania. '''
        self.__actions.sort( cmp=pos_cmp )

    def perform_up_to(self, position_x=None):
        ''' Wyzwala wszystkie akcje, których pozycja jest niewiększa niż position_x. Jeśli
        position_x=None, to zostaną uruchomione wszystkie akcje (oczywiście najpierw najstarsze).'''
        for action in self.__actions:
            if position_x==None or action.get_position_x()<=position_x:
                action.perform()
            else:
                break  # jeżeli akcja nie powinna być uruchomiona, to następne tym bardziej


### OBIEKTY ###

class LevelObject(LevelAction):
    ''' Klasa akcji. Odpowiada z tworzenie obiekt w poziomie.'''

    def __init__(self, pos, screenPos, objectName):
        assert isinstance(pos, tuple), "argument pos musi byc krotka a nie %s" % type(pos)
        assert len(pos)==2, "krotka pos musi miec dokladnie dwa elementy a nie %d" % len(pos)
        assert isinstance(screenPos, tuple), "argument screenPos musi byc krotka a nie %s" % type(screenPos)
        assert len(screenPos)==2, "krotka screenPos musi miec dokladnie dwa elementy a nie %d" % len(screenPos)
        self.__position = map( lambda arg:float(arg), pos )
        self.__screenPosition = map( lambda arg:float(arg), screenPos )
        self.__objectName = objectName

    def perform(self):
        print "tworzenie obiektu `%s` na pozycji" % self.get_name(), self.get_position()

    def get_position_x(self):
        return self.__position[0]

    def get_position(self):
        return self.__position

    def get_screen_position(self):
        return self.__screenPosition

    def get_name(self):
        return self.__objectName
    
class LevelObjectManager:
    ''' Klasa menedżera obiektów odpowiada za zarządzeniem obiektami w poziomie.'''

    def __init__(self, objects):
        ''' Inicjuje menedżer podaną listą obiektów. '''
        self.__objects = objects
        self.__sort_objects()

    def __sort_objects(self):
        ''' Sortuje listę obiektów według kolejności występowania. '''
        self.__objects.sort( cmp=pos_cmp )

    def get_all_objects(self):
        ''' Zwraca posortowaną listę wszystkich obiektów.'''
        return self.__objects

    def get_objects_between_x(self, x_start, x_end):
        ''' Zwraca posortowaną listę obiektów, których współrzędna x nalezy do zbioru (x_start,x_end). '''
        objects = []
        for obj in self.__objects:
            if obj.get_position_x() >= x_end:  # jeżeli obiekt jest dalej niż x_end,...
                break           # ... to wszystkie następne też
            if obj.get_position_x() > x_start:
                objects.append( obj )
        return objects


### DEFINICJE ###

class LevelDefiniton:
    ''' Klasa bazowa opisująca definicję w poziomie.'''

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

class SpriteLevelDefinition(LevelDefiniton):
    ''' Klasa definicji. Opisuje definicję sprite'a w poziomie.'''

    def __init__(self, name, animName):
        LevelDefiniton.__init__(self, name)
        self.__animationName = animName

    def get_animation_name(self):
        return self.__animationName
    
class DefinitionManager:
    ''' Klasa menedżera definicji odpowiada za zarządzanie definicjami w poziomie.'''

    def __init__(self, definitions):
        ''' Inicjuje menedżer podaną listą definicji. '''
        self.__definitions = definitions

    def get_definition(self, name):
        definitions = [defn for defn in self.__definitions if defn.get_name()==name ]
        if definitions: return definitions[0]
        else: return None

### PODŁOŻE ###

class GroundPart:
    ''' Klasa opisująca jeden element podłoża. '''

    def __init__(self, name):
        assert isinstance(name,basestring), "W konstruktorze należy jako nazwę podać ciąg znaków. Podano typ %s" % type(name)
        self.__name = name
        self.__position = (0,0)

    def get_name(self):
        return self.__name

    def set_position(self,position):
        self.__position = position

    def get_position(self):
        return self.__position

    def get_position_x(self):
        return self.get_position()[0]

class GroundManager:
    ''' Klasa menedżera podłoża. Agreguje obiekty klasy GroundPart.'''

    def __init__(self, grounds):
        ''' Tworzy menedżer z elementami podłoża przekazanymi w grounds.'''
        self.__grounds=grounds

    def append_ground(self, groundPart, pos):
        ''' Dodaje kawałek podłoża do menedżera w miejsce pos. Jeżeli pos=None, to wstawia na koniec.
        Zwraca status powodzenia (True-dodanie powiodło się).'''
        assert isinstance(groundPart,GroundPart), "Kawałek podłoża musi być typu GroundPart. Jest typu %s." % type(groundPart)
        if pos==None:
            self.__grounds.append(groundPart)
        else:
            print "Wstawianie podłoża w środek nie jest zaimplementowane."
            return False
        return True

#     def get_grounds(self, startPos, endPos, delete=False):
#         ''' Zwraca informacje o podłożach między startPos i endPos. Jeżeli delete=True,
#         to zostaną usunięte podłoża o pozycjach mniejszych niż startPos. '''
#         assert False, "Not implemented"
#         grounds = []
#         #
#         # TODO: przelicz, które podłoża należy zwrócić
#         #
#         # if należy_zwrócić(ground):
#         #    grounds.append(ground)
#         return grounds

#     def get_grounds(self):
#         return map(lambda g:g.get_name(), self.__grounds)

    def get_all_grounds(self):
        return self.__grounds

class BackgroundManager:
    ''' Klasa menedżera tła.'''
    def __init__(self):
        self.__filenames = []

    def append_filename(self,filename):
        self.__filenames.append(filename)

    def get_filenames(self):
        return self.__filenames


### ELEMENTY PEJZAŻU ###
class SceObject(object):
    ''' Klasa akcji. Odpowiada z tworzenie obiekt w poziomie.'''

    def __init__(self, pos, screenPos, objectName):
        assert isinstance(pos, tuple), "argument pos musi byc krotka a nie %s" % type(pos)
        assert len(pos)==2, "krotka pos musi miec dokladnie dwa elementy a nie %d" % len(pos)
        assert isinstance(screenPos, tuple), "argument screenPos musi byc krotka a nie %s" % type(screenPos)
        assert len(screenPos)==2, "krotka screenPos musi miec dokladnie dwa elementy a nie %d" % len(screenPos)
        self.__position = map( lambda arg:float(arg), pos )
        self.__screenPosition = map( lambda arg:float(arg), screenPos )
        self.__objectName = objectName

    def perform(self):
        print "tworzenie elementu pejzażu `%s` na pozycji" % self.get_name(), self.get_position()

    def get_position_x(self):
        return self.__position[0]

    def get_position(self):
        return self.__position

    def get_screen_position(self):
        return self.__screenPosition

    def get_name(self):
        return self.__objectName

class SceObjectManager(object):
    ''' Klasa menedżera obiektów odpowiada za zarządzeniem obiektami w poziomie.'''

    def __init__(self, objects):
        ''' Inicjuje menedżer podaną listą obiektów. '''
        self.__objects = objects
        self.__objects.sort( cmp=pos_cmp )

    def get_all_objects(self):
        ''' Zwraca posortowaną listę wszystkich obiektów.'''
        return self.__objects

    def get_objects_between_x(self, x_start, x_end):
        ''' Zwraca posortowaną listę obiektów, których współrzędna x nalezy do zbioru (x_start,x_end). '''
        objects = []
        for obj in self.__objects:
            if obj.get_position_x() >= x_end:  # jeżeli obiekt jest dalej niż x_end,...
                break           # ... to wszystkie następne też
            if obj.get_position_x() > x_start:
                objects.append( obj )
        return objects

### LEVEL PARSER ###

class LevelParser:
    '''Klasa odczytująca poziom z pliku. Zwraca status powodzenia.'''

    def __init__(self, filename):
        self.__levelAuthor="[Gal Anonim]"        # domyślne wartości
        self.__levelName="[no level name]"
        self.__errors = []

        # spróbuj wczytać plik jako DOM
        print 'Loading level from `%s`...' % filename
        data = xmlDom.parse(filename)
        if not data.hasChildNodes():
            print 'FAILED. Nie znalezono dzieci dla pierwszego elementu.'
            errors.append('FAILED. Nie znalezono dzieci dla pierwszego elementu.')

        #
        # TODO
        # sprawdzenie poprawności przez xml.sax
        #

        # sprawdź czy plik zaczyna sie od tagu <level>
        levels = [ node for node in data.childNodes if node.nodeName=='level' ]
        lvl = levels[0] if len(levels)>0 else None
        if lvl==None:
            print 'Nieprawidłowy pierwszy tag, oczekiwano `level`'
            return errors.append('Nieprawidłowy pierwszy tag, oczekiwano `level`')

        # wczytaj dane dotyczące poziomu (nagłówek, akcje, tło, definicje,...)
        # Musimy zapewnić, że węzły 'header' i 'definitions' zostaną wczytane przed innymi,
        # które mogą z nich korzystać (np. w nagłówku mogą być jakieś info o wersji)
#         self.__actionManager = None
#         self.__definitionManager = None
        levelNodes = lvl.childNodes
        nodes = [node for node in levelNodes if node.localName=='header']
        nodes+= [node for node in levelNodes if node.localName=='definitions']
        nodes+= [node for node in levelNodes if not node.localName in ['header','definitions'] ]
        for node in nodes:
            if node.nodeType==data.ELEMENT_NODE:
                if node.localName=='header':      self.__parse_header(node)
                if node.localName=='definitions': self.__definitionManager = self.__parse_definitions(node)
                if node.localName=='ground':      self.__groundManager = self.__parse_ground(node)
                if node.localName=='actions':     self.__actionManager = self.__parse_actions(node)
                if node.localName=='objects':     self.__objectManager = self.__parse_objects(node)
                if node.localName=='scenery':     self.__sceManager = self.__parse_scenery(node)
                if node.localName=='background':  self.__backgroundManager = self.__parse_background(node)

    def get_errors(self):
        return self.__errors

    def __parse_header(self, node):
        '''Przetwarza nagłówek.'''
        print 'parsing header'

        # wyłuskaj autora
        authorList = node.getElementsByTagName('author')
        self.__levelAuthor = authorList[0].childNodes[0].data if len(authorList)>0 else self.__levelAuthor

        # wyłuskaj nazwę poziomu
        namesList = node.getElementsByTagName('name')
        self.__levelName = namesList[0].childNodes[0].data if len(namesList)>0 else self.__levelName
        print "\tauthor = `%s`, \n\tlevelName = `%s`" % (self.__levelAuthor, self.__levelName)

    def __parse_definitions(self, node):
        '''Przetwarza definicje.'''
        print 'parsing definitions'
        self.__definitions = []
        # znajdź wszystkie definicje
        for defn in node.getElementsByTagName('definition'):
            name = defn.getAttribute('name') if defn.hasAttribute('name') else "[no name]"
            for sprite in defn.getElementsByTagName('sprite'):
#                 fname = sprite.getAttribute('filename') if sprite.hasAttribute('filename') else ''
                aname = sprite.getAttribute('animation') if sprite.hasAttribute('animation') else ''
                print "\tsprite \n\t\tanimation=`%s`" % (aname)
#                 self.__definitions.append( SpriteLevelDefinition(name=name,filename=fname,animName=aname) )
                self.__definitions.append( SpriteLevelDefinition(name=name,animName=aname) )
        # zwróć menedżer definicji
        return DefinitionManager( self.__definitions )


    def __parse_actions(self, node):
        '''Przetwarza akcje.'''
        print 'parsing actions'
        self.__actions = []

        # szukaj akcji: Stop Scrolling
        for stScroll in node.getElementsByTagName('stopScrolling'):
            for pos in stScroll.getElementsByTagName('position'):
                x = pos.getAttribute('x') if pos.hasAttribute('x') else 0
            print "\tstopScrolling"
            # dodaj nowy obiekt do listy akcji
            self.__actions.append( StopScrollingLevelAction( pos=float(x) ) )
        # zwróć menedżer akcji
        return LevelActionManager( self.__actions )

    def __parse_objects(self, node):
        ''' Przetwarza tworzenie obiektów. '''
        print 'parsing objects.'
        objs = []
        # szukaj obiektów
        for cobj in node.getElementsByTagName('object'):
            print "\tobject"
            name = cobj.getAttribute('name') if cobj.hasAttribute('name') else "[no name]"
            for pos in cobj.getElementsByTagName('position'):
                x = pos.getAttribute('x') if pos.hasAttribute('x') else 0
#                  y = pos.getAttribute('y') if pos.hasAttribute('y') else 0
#                  print "\t\tposition with x=%f , y=%f" % (float(x), float(y))
                print "\t\tposition with x=%f" % float(x)
            for screenPos in cobj.getElementsByTagName('screen_position'):
                sx = screenPos.getAttribute('x') if screenPos.hasAttribute('x') else 0
                sy = screenPos.getAttribute('y') if screenPos.hasAttribute('y') else 0
                print "\t\tscreen position with x=%f , y=%f" % (float(sx), float(sy))
            # dodaj nowy obiekt do listy akcji
            y = 0        # atrybut y jest zbędny
            position = (float(x),float(y))
            screenPosition = (float(sx),float(sy))
            objs.append( LevelObject( pos=position, screenPos=screenPosition, objectName=name ) )
        return LevelObjectManager( objs )

    def __parse_ground(self, node):
        '''Przetwarza dane związane z podłożem.'''

        print 'parsing ground'
        self.__grounds = []
#         prevPart = None            # poprzedni element - potrzebne aby dodać połączenie
#         prevJoin = False           # czy poprzedni element wymaga łączenia?
        for part in node.getElementsByTagName('part'):
            print "\tpart"
            name = repeat = useJoin = None
            if part.hasAttribute('name'):
                name = part.getAttribute('name')
                print "\t\tname = %s" % name
            if part.hasAttribute('repeat'):
                repeat = int(part.getAttribute('repeat'))
                print "\t\trepeat = %s" % repeat
#             if part.hasAttribute('joinWithNext'):
#                 joinWithNext = True if part.getAttribute('joinWithNext')=='true' else False
#                 print "\t\tjoinWithNext = %s" % joinWithNext
            if part.hasAttribute('useJoin'):
                useJoin = True if part.getAttribute('useJoin')=='true' else False
                print "\t\tuseJoin = %s" % useJoin
            # sprawdź czy wszystkie atrybuty zostały wczytane
            assert name!=None, "brak atrybutu name"
            assert repeat!=None, "brak atrybutu repeat"
#             assert joinWithNext!=None, "brak atrybutu joinWithNext"
#             part = GroundPart( name=name )
#             # dodaj połączenie między częściami, jeśli konieczne
#             if prevPart!=None and prevJoin and (prevPart.get_name() != part.get_name()):
#                 self.__grounds.append( GroundPart(prevPart.get_name() + ',' + part.get_name()) )
            # dodaj element podłoża tyle razy ile producent każe ;)
            for i in range(repeat):
                part = GroundPart( name=name )
                self.__grounds.append( part )
#             prevPart = part
#             prevJoin = joinWithNext
        # zwróć menedżer podłoża
        return GroundManager( self.__grounds )

    def __parse_background(self, node):
        '''Przetwarza dane związane z tłem.'''
        print 'parsing background'
        bm = BackgroundManager()
        for part in node.getElementsByTagName('part'):
            print "\tpart"
            if part.hasAttribute('name'):
                name=part.getAttribute('name')
                print "\t\tname = %s" % name
            if part.hasAttribute('filename'):
                filename=part.getAttribute('filename')
                print "\t\tfilename = %s" % filename
                bm.append_filename(filename)
            if part.hasAttribute('repeat'):
                repeat=part.getAttribute('repeat')
                print "\t\trepeat = %s" % repeat
        return bm


    def __parse_scenery(self, node):
        '''Przetwarza dane związane z pejzażem.'''
        print 'parsing scenery'
        objs = []
        for cobj in node.getElementsByTagName('part'):
            print "\tpart"
            name = cobj.getAttribute('name') if cobj.hasAttribute('name') else "[no name]"
            for pos in cobj.getElementsByTagName('position'):
                x = pos.getAttribute('x') if pos.hasAttribute('x') else 0
#                  y = pos.getAttribute('y') if pos.hasAttribute('y') else 0
#                  print "\t\tposition with x=%f , y=%f" % (float(x), float(y))
                print "\t\tposition with x=%f" % float(x)
            for screenPos in cobj.getElementsByTagName('screen_position'):
                sx = screenPos.getAttribute('x') if screenPos.hasAttribute('x') else 0
                sy = screenPos.getAttribute('y') if screenPos.hasAttribute('y') else 0
                print "\t\tscreen position with x=%f , y=%f" % (float(sx), float(sy))
            # dodaj nowy obiekt do listy akcji
            y = 0        # atrybut y jest zbędny
            position = (float(x),float(y))
            screenPosition = (float(sx),float(sy))
            objs.append( SceObject( pos=position, screenPos=screenPosition, objectName=name ) )
        return SceObjectManager( objs )


    def get_level_author(self):
        '''Zwraca autora poziomu.'''
        return self.__levelAuthor

    def get_level_name(self):
        '''Zwraca nazwę/tytuł poziomu.'''
        return self.__levelName


    def get_action_manager(self):
        '''Zwraca menedżer akcji w poziomie.'''
        return self.__actionManager

    def get_object_manager(self):
        '''Zwraca menedżer obiektów w poziomie.'''
        return self.__objectManager

    def get_definition_manager(self):
        '''Zwraca menedżer definicji w poziomie.'''
        return self.__definitionManager

    def get_ground_manager(self):
        '''Zwraca menedżer podłoża w poziomie.'''
        return self.__groundManager

    def get_sce_manager(self):
        '''Zwraca menedżer pejzazy w poziomie.'''
        return self.__sceManager

    def get_background_manager(self):
        '''Zwraca menedżer tła w poziomie.'''
        return self.__backgroundManager
