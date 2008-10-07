#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Moduł parsujący plik skryptu sprite'a.
'''

import re
import os.path

class SpriteLogicInfo(object):
    ''' Agregat informacji o animacji sprite'a. Agreguje wszystkie
    inforamcje potrzebne przy zmianie stanu animacji (np. zmianie
    klatki) '''

    def __init__(self):
        self.frames_count = None
        self.duration     = None

        
class SpriteAnimationInfo(object):
    ''' Agreguje informacje potrzebne przy wyłuskiwaniu aktualnej
    klatki animacji z tekstury '''
    
    def __init__(self):
        self.x_offset     = None
        self.y_offset     = None
        self.fame_width   = None
        self.frame_height = None
        self.cols_count   = None


class SpriteScriptParser(object):
    ''' Parsuje pliki skryptowe sprite'ów. Udostępnia wczytane
    informacje '''

    def __init__(self, spriteName):
        self.__filename = os.path.join('..','gfx',spriteName,'script.sprite')
        self.__logic_part = {}  # słownik nazwa_animacji => SpriteLogicInfo
        self.__sprite_part = {} # słownik nazwa_animacji => SpriteAnimationInfo
        self.__spriteLoaded = False # czy sprite został już załadowany
        self.__debug = False    # czy wypisywać informacje diagnostyczne


    def get_logic_part(self):
        ''' Zwraca informacje potrzbne do zarządzania logiką sprite'a '''
# FIXME:        if not self.__spriteLoaded: raise ???
        return self.__logic_part
    

    def get_sprite_part(self):
        ''' Zwraca informacje potrzebne do zarządzania teksturą sprite'a '''
# FIXME:        if not self.__spriteLoaded: raise ???        
        return self.__sprite_part


    def parse(self):
        ''' Parsuje plik skryptu. Wyciąga z niego wszystkie informacje
        potrzebne do zarządzania spritem i wyświetlania go '''
        
        lines = self.__split_script()       # podziel skrypt na linie
        (rs, commentStr) = self.__create_regex_table() # stwórz tablicę wyrażeń regularnych

        # przetwarzanie wczytanych danych
        animationName = None         # nazwa animacji

        for i,line in enumerate(lines):
            i = i+1    # popraw numerację. Normalnie liczymy linie od 1
            line = line.split( commentStr )[0]   # FIXME wyrzuć komentarze
            
            # spróbuj dopasować linię do któregoś wzorca
            lineMatches = False
            for reKey, reVal in rs.items():
                reMatch = re.compile( reVal ).match( line )

                if reMatch:
                    lineMatches = True     # dopasowano linię
                    matchResult = self.__unpack( reMatch.groups() ) # pobierz wynik dopasowania
                    if self.__debug:
                        print "Linia %2d dopasona jako %s (%s)" % (i,reKey,matchResult)

                    animationName = self.__match_line(reKey, matchResult, animationName)

            if not lineMatches:
                print 'ERROR: niepoprawna linia %d w pliku %s' % (i,self.filename)
                return False
            
        self.__spriteLoaded = True
        return True


    def __split_script(self):
        ''' Dzieli plik skryptu na linie '''
        lines = None      # linie wczytane z pliku
        
        try:
            f = open(self.__filename,'rU')
            lines = f.readlines()
            f.close()
        except:
            print "ERROR: nieznaleziono pliku sprite\'a lub plik jest uszkodzony:", self.__filename
#            raise "" ???
            
        return lines
            

    def __create_regex_table(self):
        ''' definicja lini w pliku (jako wyrażenia regularne) '''
        commentStr = '--'       # ciąg rozpoczynający komentarz
        rs = {
            'emptyLine'   : '\s*$',
            'comment'     : '\s*'+commentStr+'(.*?)$',
            'duration'    : '\s*DURATION\s*=\s*([0-9]+)\s*$',
            'frames_count': '\s*FRAMES_COUNT\s*=\s*([0-9]+)\s*$',
            'anim'        : '\s*ANIMATION\s*=\s*[\'"](.*?)[\'"]\s*$',
            'frame_width' : '\s*FRAME_WIDTH\s*=\s*([0-9]+)\s*$',
            'frame_height': '\s*FRAME_HEIGHT\s*=\s*([0-9]+)\s*$',
            'cols'        : '\s*COLS_COUNT\s*=\s*([0-9]+)\s*$',
            'xoff'        : '\s*X_OFFSET\s*=\s*([0-9]+)\s*$',
            'yoff'        : '\s*Y_OFFSET\s*=\s*([0-9]+)\s*$'
            }
        
        return (rs, commentStr)

    
    def __unpack(self, tup):
        ''' Pobiera krotke i wykrywa w niej ciągi, które są liczbami.
        Ciagi wypakowuje z apostrofów i cudzysłowiów. '''
        ret = []
        for v in tup:
            try:  ret.append( int(float(v)) )         # try convert to int
            except: ret.append( v.strip( '\'" \t' ) )  # cut '," and whitespaces
        return (ret[0] if len(ret)==1 else tuple(ret))

    
    def __match_line(self, reKey, matchResult, animationName):
        ''' Przekształca dopasowanie linii w informacje dla sprite'a '''
        if reKey == 'emptyLine':        # olej puste linie
            return animationName
        
        elif reKey == 'anim':           # definicja nowej animacji
            animationName = matchResult
            self.__logic_part[ animationName ] = SpriteLogicInfo()
            self.__sprite_part[ animationName ] = SpriteAnimationInfo()
            
        else:         # jakaś komenda w animacji
            if animationName == None:
                print "ERROR: w lini %d, komenda bez zdefiniowanej animacji" % i
                return False
            
            # Instrukcje związane z logiką
            if reKey == 'duration'         : self.__logic_part[ animationName ].duration      = matchResult
            elif reKey == 'frames_count'   : self.__logic_part[ animationName ].frames_count  = matchResult
            
            # Instrukcje związane z samą animacją
            elif reKey == 'frame_width'    : self.__sprite_part[ animationName ].frame_width  = matchResult
            elif reKey == 'frame_height'   : self.__sprite_part[ animationName ].frame_height = matchResult
            elif reKey == 'cols'           : self.__sprite_part[ animationName ].cols_count   = matchResult
            elif reKey == 'xoff'           : self.__sprite_part[ animationName ].x_offset     = matchResult
            elif reKey == 'yoff'           : self.__sprite_part[ animationName ].y_offset     = matchResult

        return animationName
