# #!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# skrypt należy uruchomić jako argument podając plik z danymi sprite'a, #
# czyli np. python spriteTest.py heli.sprite                            #
# zostanie wyświetlona domyślna animacja.                               #
# Zmiana animacji jest na razie niemożliwa                              #
#########################################################################


import pyglet
from pyglet import resource, image
from pyglet.gl import *
from pyglet.window import key
import re
import sys

class Sprite:
    def __init__(self):
        self.__spriteLoaded = False  # czy animacje zostały załadowane so sprite'a
        self.__filename = ''         # nazwa pliku z danymi sprite'a
        self.__animations = {}       # animacje sprite'a
        self.__imageFilename = ''    # nazwa pliku z obrazkami dla sprite'a

        # poniższe zmienne odpowiadają za animację
        # w przyszłości pewnie ich tu nie będzie 
        self.prevAnim = ''
        self.currFrame = 0


    def load_from_file(self, filename):
        ''' Ładuje animacje z pliku ze spritem. Zwraca status powodzenia.'''
        self.__filename = filename
        self.__animations = {}
        self.__imageFilename = ''
        self.__spriteLoaded = False

        # wczytaj linie z pliki i zapisz jako liste linijek
        lines = None      # linie wczytane z pliku
        try:
            f = open(self.__filename,'rU')
            lines = f.readlines()
            f.close()
        except:
            print "Error: nieznaleziono pliku lub plik uszkodzony:", self.__filename
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
                print 'Error: niepoprawna linia %d w pliku %s' % (i,self.__filename)
                return False
        # dodaj ostatnią animację 
        if len(animation):
            self.__animations[ animationName ] = animation

#         print self.__animations, self.__imageFilename
        self.__spriteLoaded = True
        self.assertme()
        return True


    def set_animation(self, animName, reload=False):
        ''' Ustawia dane żądanej animacji.
        reload - Wymusza rozpoczęcie animacji od 0. klatki.
        Zwraca False jeżeli ustawienie animacji się nie powiodło. '''

        self.assertme()

        if not self.__spriteLoaded:
            print "Error: nie ma żadnych animacji do wyświetlenia. Czy zostały wczytane?"
            return False

        ''' FIXME poniższym prawdopodobnie powinna zajmować się już inna klasa. '''
        # 
        if self.prevAnim != animName or reload:
            self.prevAnim = animName
            print 'Próba zmiany animacji w %s na %s' % (self.__filename,animName)
            self.currFrame = 0

        anim = self.__animations[animName] if self.__animations.has_key(animName) else {}
        if anim:
            imgFilename = self.__imageFilename
            try:
                self.tex = image.load( imgFilename ).get_texture() if imgFilename else None
            except:
                print "Error: ładowanie tekstury z pliku nie powiodło się (%s)" % imgFilename
                return False
            try:
                self.yoff = (anim['yoff'] if anim.has_key('yoff') else 0)  # default
                self.xoff = (anim['xoff'] if anim.has_key('xoff') else 0)  # default
                self.frameNum = anim['frames_count']
                self.duration = anim['duration'] / self.frameNum / 1000.0
                self.wid, self.hei = anim['frame']
                self.colNum = anim['cols']
            except KeyError,arg:
                print 'Error: brakujący klucz (',arg,'). Dane źle wczytane?'
                return False
        else:
            print 'Error: nie ma takiej animacji (',animName,')'
            return False
        return True

    def assertme(self):
        ''' Jakies self-testy spójności. '''
        pass


class App:
    def __init__(self):
        self.time = 0.0      # sumaryczny czas działania aplikacji

        # jakieś zmienne do animacji sprite'a
        self.playAnim = 0
        self.playFrame = 0
        self.prevTime = 0


    def load(self):
        self.s = Sprite()
        if len(sys.argv)<2:
            print "Jako argument podaj plik z definicją sprite'a"
            return False
        spriteName = sys.argv[1]
        if not self.s.load_from_file( spriteName ):
            print "Sprite %s loading failed" % spriteName
            return False
        return True


    def on_update(self, dt):
        self.time += dt


    def on_draw(self):
        glClearColor( .5, .6, .6, 1 )
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        ww,wh = window.width//2, window.height//2
        
        animes = ['']
        glScalef( 1, 1, 1 )
        self.draw_sprite( self.s, (0,0,0), animes[self.playAnim] )


    def on_key_press(self,symbol,mods):
#         if symbol == key.B:
#             self.playAnim = 0
#             self.playFrame = 0
#         if symbol == key.Y:
#             self.playAnim = 1
#             self.playFrame = 0
            
        print 'Pressed:',symbol,' with', mods
        if symbol == key.ESCAPE:
            sys.exit()
        return pyglet.event.EVENT_HANDLED


    def draw_sprite( self, sprite, scrPos, anim ):
        # ustaw opengl (teksturowanie, blending)
        glPushMatrix()
        if sprite.set_animation( anim ):
            glColor4f( 1, 1, 1, 1 )
            glEnable( GL_BLEND )
            glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
            glEnable( sprite.tex.target )
            glBindTexture( sprite.tex.target, sprite.tex.id )

            # obliczenia niezbędne do narysowania sprite'a
            if self.prevTime + sprite.duration  <= self.time:
                self.prevTime = self.time
                sprite.currFrame = sprite.currFrame + 1
            sprite.currFrame = sprite.currFrame % sprite.frameNum
            row,col = divmod( sprite.currFrame, sprite.colNum )
            texWid, texHei = float(sprite.tex.width), float(sprite.tex.height)
            left   =  col    * sprite.wid / texWid
            right  = (col+1) * sprite.wid / texWid
            top    = (sprite.yoff +  row    * sprite.hei) / texHei
            bottom = (sprite.yoff + (row+1) * sprite.hei) / texHei
#             print sprite.duration
#             print sprite.yoff
#             print row,col
#             print left, right, top, bottom
#             print 

            # narysuj oteksturowany czworokąt
            glTranslatef( *scrPos )
            glBegin( GL_QUADS )
            tc = ( (left,1-bottom), (right,1-bottom), (right,1-top), (left,1-top) )
            vs = ( (0,0), (sprite.wid,0), (sprite.wid, sprite.hei), (0, sprite.hei) )
            for t,v in zip(tc,vs):
                glTexCoord2f( *t )
                glVertex2f( *v )
            glEnd()
        glPopMatrix()


window = pyglet.window.Window( 800, 600, caption='Sprite test' )

@window.event
def on_key_press(symbol, mods):
    global app
    return app.on_key_press( symbol, mods )

@window.event
def on_draw():
    global app
    return app.on_draw()

def update(dt):
    global app
#     print pyglet.clock.get_fps(), dt
    return app.on_update(dt)

pyglet.clock.schedule_interval( update, 1.0/35 )
# pyglet.clock.schedule( update )


app = App()
if app.load():
    pyglet.app.run()
