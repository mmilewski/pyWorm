#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Moduł zawiera klasę zarządzającą sprite'ami oraz klasę opisującą jedną klatkę animacji.'''

from pyglet import image

from spriteScriptParser import SpriteAnimationInfo

class SpriteAnimationFrame:
    ''' Informacje o pojedynczej klatce animacji
    sprite'a. Wykorzystywane jako wartość zwracana
    GameObject::get_frame '''

    def __init__(self, textureId, drawRect, frameWidth, frameHeight ):
        ''' Tworzy klatkę animacji sprite'a.
        textureId - tekstura, na której jest klatka do narysowania.
        drawRect - krotka (xLewy, yDół, xPrawy, yGóra) opisując, który fragment
        tekstury należy narysować (gdzie znajduje się klatka).'''
        self.textureId   = textureId
        self.rect        = drawRect
        self.width       = frameWidth
        self.height      = frameHeight

        
class SpriteManager:
    ''' Zarządza sprite'ami od strony grafiki. Logiką zarządzają same
    obiekty przez SpriteScriptStrategy, które jest ładowane przez
    SpriteScriptParser. Zadanime SpriteManager'a jest jedynie
    przechowywać informacje o teksurach sprite'a i udostępniać na
    żądanie konkretne klatki (w tym celu przechowuje część informacji
    ze skryptu sprite'a) '''
    
    def __init__(self):
        self.__sprites = {}                 # słownik par (textureId, słownik animacji - spriteScripts, textureWidth, textureHeight, image.alpha_data, image.width )
        self.__textures = []                # pamiętane, aby GC nie namieszał

        
    def load_sprite(self, spriteName, spriteScript):
        ''' Dodaje skrypt do menadżera. '''
        (textureId, img) = self.__sprite_name_to_texture(spriteName)
        self.__sprites[ spriteName ] = (textureId, spriteScript, float(img.width), float(img.height), img.get_data("A", -img.width), img.width)

        
    def __sprite_name_to_texture(self, spriteName):
        ''' pobiera nazwę sprite'a i ładuje odpowiednią teksturę z
        dysku. Zwraca teksturę i odpowiedni obrazek '''
        spriteImagePath = "../gfx/" + spriteName + "/image.png"
        
        img       = image.load(spriteImagePath)
        texture   = img.get_texture()
        textureId = texture.id

        self.__textures.append(texture)
        
        return (textureId, img)


    def get_frame( self, spriteName, animationName, frameNum ):
        ''' Zwraca klatkę do narysowania obiektu o - obiekt typu SpriteAnimationFrame '''
        animation = self.__sprites[ spriteName ][ 1 ][ animationName ]
        
        texWidth  = self.__sprites[ spriteName ][ 2 ]
        texHeight = self.__sprites[ spriteName ][ 3 ]

        texLeft   = animation.x_offset + frameNum * animation.frame_width
        texTop    = texHeight - animation.y_offset
        
        if animation.x_offset + frameNum * animation.frame_width >= texWidth:
            frameNum -= (texWidth - animation.x_offset) / animation.frame_width
            texLeft  %= animation.cols_count * animation.frame_width
            texTop   += (frameNum / animation.cols_count) *  animation.frame_height
            
        texRight  = texLeft + animation.frame_width
        texBottom = texTop - animation.frame_height

        # normalizacja współrzędnych (przejście z width i height do 0..1)
        texLeft   /= texWidth
        texRight  /= texWidth
        texTop    /= texHeight
        texBottom /= texHeight

        # obliczanie id tekstury
        textureId = self.__sprites[ spriteName ][ 0 ]

        return SpriteAnimationFrame( textureId,
                                     (texLeft, texBottom, texRight, texTop),
                                     animation.frame_width,
                                     animation.frame_height )    


    def __get_object_frame( self, o ):
        ''' Zwraca klatkę do narysowania obiektu o - obiekt typu SpriteAnimationFrame '''        
        return self.get_frame(o.spriteName,
                              o.get_current_animation_name(),
                              o.get_current_frame_num())


    
    def __get_sprite_pixel( self, spriteName, x, y ):
        ''' Zwraca piksel o współrzędnych x,y sprite'a spriteName '''
        width = self.__sprites[spriteName][5]
        return self.__sprites[spriteName][4][y * width + x]


    def __get_sprite_frame_pixel( self, o, x, y ):
        ''' Zwraca piksel o współrzędnych x,y aktualnej klatki animacji obiektu o '''
        frame = self.__get_object_frame(o)
        
        xbase = frame.width * o.get_current_frame_num()
        ybase = 0 # ???
        
        return self.__get_sprite_pixel( o.spriteName, xbase + x, ybase + y)


    def check_per_pixel_collision( self, o1, o2 ):
        ''' Sprawdza czy jeżeli na sprite'a obiektu o1 nałożymy
        sprite'a obiektu o2 w pozycji delta (jest to przesunięcie
        lewego dolnego rogu o2 względem lewego dolnego rogu o1), to
        czy istnieją dwa pikesele które nachodzą na siebie (czyli czy
        przecięcie miejsc gdzie oba nie mają kanału alfa 0 jest
        niepuste).'''

        # # Do testów warto wyłączać kolizję aby zmniejszyć output
        # excluded = ["grass", "hill", "stone", "bridge"]
        # if o1.spriteName in excluded or o2.spriteName in excluded:
        #     return False

        # # debug info
        # print "Sprite names   : ", o1.spriteName, o2.spriteName
        # print "Animation names: ", o1.get_current_animation_name(), o2.get_current_animation_name()
        # print "Frame nums     : ", o1.get_current_frame_num(), o2.get_current_frame_num()
        # print "Positions      : ", o1.position, o2.position


        # Ustawiamy obiekty po x, aby było mniej przypadków
        if o1.position[0] > o2.position[0]:
            t = o1
            o1 = o2
            o2 = t
        
        # oblicz szerokość i wysokość (w,h) przecięcia aabb spritów
        # oblicz współrzędne lewego dolnego rogu przecięcia aabb
        # spritów względem sprite'a 1 (x1,y1) i sprite'a 2 (x2,y2)
        dx = int((o2.position[0] - o1.position[0]) * 1000) # 800
        dy = int((o2.position[1] - o1.position[1]) * 750)  # 600

        frame1 = self.__get_object_frame(o1)
        frame2 = self.__get_object_frame(o2)
        
        if dy >= 0:
            x1 = dx
            y1 = frame1.height - dy
            x2 = 0
            y2 = frame2.height - 0
            w  = min([frame2.width, frame1.width - dx])
            h  = min([frame2.height, frame1.height - dy])
        else:
            x1 = dx
            y1 = frame1.height - 0
            x2 = 0
            y2 = frame2.height + dy
            w  = min([frame2.width, frame1.width - dx])
            h  = min([frame1.height, frame2.height + dy])


        # Obliczamy informacje potrzebne do 
        width1 = self.__sprites[o1.spriteName][5]
        xbase1 = frame1.width * o1.get_current_frame_num()
        ybase1 = 0 # ???

        width2 = self.__sprites[o2.spriteName][5]
        xbase2 = frame2.width * o2.get_current_frame_num()
        ybase2 = 0 # ???
        
        for y in range(-h, 0):
            for x in range(0, w):
                # Tu były te wywołania, ale Python ma bardzo dużą karę
                # za wywołania funkcji :-/ Dlatego są poniżej wklejone definicje
                # 
                # pix1 = self.__get_sprite_frame_pixel(o1, x + x1, y + y1)
                # pix2 = self.__get_sprite_frame_pixel(o2, x + x2, y + y2)
                pix1 =  self.__sprites[o1.spriteName][4][(ybase1 + y + y1) * width1 + (xbase1 + x + x1)]
                pix2 =  self.__sprites[o2.spriteName][4][(ybase2 + y + y2) * width2 + (xbase2 + x + x2)]                
                if ord(pix1) > 128 and ord(pix2) > 128:
                    return True
        return False
            
        # #             
        # # DEBUG OUTPUT
        # # 
        # # Rysuje część wspólną obu sprite'ów. Rysuje trzy
        # # obrazki. Dla każdego ze spritów po jednym oraz jeden
        # # wspólny.
        # #
        # # . oznacza puste pole
        # # * oznacza zajęte pole
        # # # oznacza pole z kolizją
        # #
        # # UWAGA 1: Zaleca się pozostawienie tylko interesujących
        # # kolizji, bo wypisywanie na wyjście obrazków znacznie
        # # spowalnia działanie programu.
        # #
        # # UWAGA 2: Trzeba wyłączyć testy powyżej, bo inaczej do tego
        # # miejsca nigdy się nie dojdzie
        # # 
            
        # buf1 = ""
        # buf2 = ""
        # buf12 = ""
        # kolizja = False
        # for y in range(-h, 0):
        #     for x in range(0, w):
        #         c = 0
                
        #         if ord(self.__get_sprite_frame_pixel(o1, x + x1, y + y1)) > 128:
        #             buf1 += "*"
        #             c += 1
        #         else:
        #             buf1 += "."

        #         if ord(self.__get_sprite_frame_pixel(o2, x + x2, y + y2)) > 128:
        #             c += 1
        #             buf2 += "*"
        #         else:
        #             buf2 += "."

        #         if c == 0: buf12 += "."
        #         if c == 1: buf12 += "*"
        #         if c == 2: buf12 += "X"
                    
        #         pix1 = self.__get_sprite_frame_pixel(o1, x + x1, y + y1)
        #         pix2 = self.__get_sprite_frame_pixel(o2, x + x2, y + y2)
        #         if ord(pix1) > 128 and ord(pix2) > 128:
        #             kolizja = True
                    
        #     buf1 += "\n"
        #     buf2 += "\n"
        #     buf12 += "\n"
                
        # print buf1, "\n\n"
        # print buf2, "\n\n"
        # print buf12, "\n\n"
        
        # if kolizja:
        #     print "!!!! KOLIZJA !!!!"

    
    def get_aabb( self, spriteName, animationName, frameNum ):
        return (0,0,                                  # x,y (lewy dolny róg)  
                self.__sprites[ spriteName ][ 1 ][ animationName ].frame_width,
                self.__sprites[ spriteName ][ 1 ][ animationName ].frame_height)
