#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet import resource, image
import re
import os.path


class SpriteAnimation(object):
    def __init__(self, animDict, imageFilename):
        self.__imageFilename = imageFilename

        try:
            self.__texture = image.load( imageFilename ).get_texture() if imageFilename else None
        except :
            print "Error: ładowanie tekstury z pliku nie powiodło się (%s)." % imageFilename
        try:
            anim = animDict
            self.__yoff = (anim['yoff'] if anim.has_key('yoff') else 0)  # default
            self.__xoff = (anim['xoff'] if anim.has_key('xoff') else 0)  # default
            self.__frameCount = anim['frames_count']
            self.__duration = anim['duration'] / self.__frameCount / 1000.0
            self.__wid, self.__hei = anim['frame']
            self.__colCount = anim['cols']
        except KeyError, arg:
            print 'Error: brakujący klucz (',arg,'). Dane źle wczytane?'

    imageFilename = property( lambda self: self.__imageFilename )
    texture = property( lambda self: self.__texture )
    duration = property( lambda self: self.__duration )
    framesCount = property( lambda self: self.__frameCount )


class SpriteScript(object):
    ''' Opakowanie dla wartości wczytanych z pliku skryptowego. '''

#     def __init__(self, filename='', offsetXY=(0,0), frameWH=(0,0),framesCount=0, colsCount=0, duration=0 ):
#         self.__framesCount = framesCount
#         self.__colsCount = colsCount
#         self.__filename = filename
#         self.__offsetXY = offsetXY
#         self.__duration = duration
#         self.__frameWH = frameWH

    def __init__(self):
        self.__debug = False         # czy wyświetlać dodatkowe informacje?
        self.__spriteLoaded = False  # czy animacje zostały załadowane so sprite'a
        self.__filename = ''         # nazwa pliku z danymi sprite'a
        self.__animations = {}       # animacje sprite'a
        self.__imageFilename = ''    # nazwa pliku z obrazkami dla sprite'a
        self.__resourceDir = ''      # katalog z zasobami

#     framesCount = property( lambda self: self.__framesCount )
#     colsCount = property( lambda self: self.__colsCount )
#     offsetxy = property( lambda self: self.__offsetXY )
#     duration = property( lambda self: self.__duration )
#     framewh = property( lambda self: self.__frameWH )
    filename = property( lambda self: os.path.join(self.resourceDir,self.__filename) )
    imageFilename = property( lambda self: os.path.join(self.resourceDir,self.__imageFilename) )
    isLoaded = property( lambda self: self.__spriteLoaded )

    def set_resource_dir(self,val): self.__resourceDir = val
    resourceDir = property( lambda self: self.__resourceDir )


    def load_from_file(self, filename, resourceDir=''):
        ''' Ładuje animacje z pliku ze spritem. Zwraca status powodzenia.'''
        self.__filename = filename
        self.__resourceDir = resourceDir
        self.__animations = {}
        self.__imageFilename = ''
        self.__spriteLoaded = False

        # wczytaj linie z pliki i zapisz jako liste linijek
        lines = None      # linie wczytane z pliku
        try:
            f = open(self.filename,'rU')
            lines = f.readlines()
            f.close()
        except:
            print "Error: nieznaleziono pliku lub plik uszkodzony:", self.filename
            return False

        # definicja lini w pliku (jako wyrażenia regularne)
        commentStr = '--'       # ciąg rozpoczynający komentarz
        rs = { 'emptyLine': '\s*$',
               'comment': '\s*'+commentStr+'(.*?)$',
               'duration': '\s*DURATION\s*=\s*([0-9]+)\s*$',
               'frames_count': '\s*FRAMES_COUNT\s*=\s*([0-9]+)\s*$',
               'anim': '\s*ANIMATION\s*=\s*[\'"](.*?)[\'"]\s*$',
               'file': '\s*FILE\s*=\s*[\'"](.*?)[\'"]\s*$',
               'frame': '\s*FRAME\s*=\s*([0-9]+)\s*,\s*([0-9]+)\s*$',
               'cols': '\s*COLS_COUNT\s*=\s*([0-9]+)\s*$',
               'xoff': '\s*X_OFFSET\s*=\s*([0-9]+)\s*$',
               'yoff': '\s*Y_OFFSET\s*=\s*([0-9]+)\s*$'  }

        def unpack(tup):
            ''' Pobiera krotke i wykrywa w niej ciągi, które są liczbami.
                Ciagi wypakowuje z apostrofów i cudzysłowiów. '''
            ret = []
            for v in tup:
                try:  ret.append( int(float(v)) )         # try convert to int
                except: ret.append( v.strip( '\'" \t' ) )  # cut '," and whitespaces
            return (ret[0] if len(ret)==1 else tuple(ret))

        # przetwarzanie wczytanych danych
        animation = {}               # dane animacji
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
                    matchResult = unpack( reMatch.groups() ) # pobierz wynik dopasowania
                    if self.__debug:
                        print "Linia %2d dopasona jako %s (%s)" % (i,reKey,matchResult)
                    if reKey == 'emptyLine':        # olej puste linie
                        continue
                    elif reKey == 'file':           # nazwa pliku z obrazkami
                        self.__imageFilename = matchResult
                    elif reKey == 'anim':           # definicja nowej animacji
                        if len(animation):
                            self.__animations[ animationName ] = animation
                        animationName = matchResult
                        animation = { }
                    else:         # jakaś komenda w animacji
                        if animationName == None:
                            print "Erorr: w lini %d, komenda bez zdefiniowanej animacji" % i
                            return False
                        animation[ reKey ] = matchResult
                        
            if not lineMatches:
                print 'Error: niepoprawna linia %d w pliku %s' % (i,self.filename)
                return False
        # dodaj ostatnią animację 
        if len(animation):
            self.__animations[ animationName ] = animation

#         print self.__animations, self.__imageFilename
        self.__spriteLoaded = True
        self.assertme()
        return True


    def get_animation(self, animName):
        ''' Zwraca obiekt animacji odpowiadający nazwie animName lub None,
        jeżeli nie znaleziono. '''
        if not self.isLoaded:
            return None
        anim = self.__animations[animName] if self.__animations.has_key(animName) else None
        if anim:
            return SpriteAnimation( anim, self.imageFilename )
        else:
            print 'Error: nie ma takiej animacji (',animName,')'               


#     def set_animation(self, animName, reload=False):
#         ''' Ustawia dane żądanej animacji.
#         reload - Wymusza rozpoczęcie animacji od 0. klatki.
#         Zwraca False jeżeli ustawienie animacji się nie powiodło. '''

#         self.assertme()

#         if not self.isLoaded:
#             print "Error: nie ma żadnych animacji do wyświetlenia. Czy zostały wczytane?"
#             return False

#         anim = self.__animations[animName] if self.__animations.has_key(animName) else {}
#         if anim:
#             imgFilename = self.imageFilename
#             try:
#                 self.tex = image.load( imgFilename ).get_texture() if imgFilename else None
#             except:
#                 print "Error: ładowanie tekstury z pliku nie powiodło się (%s)" % imgFilename
#                 return False
#             try:
#                 self.yoff = (anim['yoff'] if anim.has_key('yoff') else 0)  # default
#                 self.xoff = (anim['xoff'] if anim.has_key('xoff') else 0)  # default
#                 self.frameNum = anim['frames_count']
#                 self.duration = anim['duration'] / self.frameNum / 1000.0
#                 self.wid, self.hei = anim['frame']
#                 self.colNum = anim['cols']
#             except KeyError,arg:
#                 print 'Error: brakujący klucz (',arg,'). Dane źle wczytane?'
#                 return False
#         else:
#             print 'Error: nie ma takiej animacji (',animName,')'
#             return False
#         return True

    def assertme(self):
        ''' Jakies self-testy spójności. '''
        pass


