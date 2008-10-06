#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        self.__sprites = {}                 # słownik par (textureId, słownik animacji - spriteScripts, textureWidth, textureHeight )
        self.__textures = []                # pamiętane, aby GC nie namieszał
        
    def load_sprite(self, spriteName, spriteScript):
        ''' Dodaje skrypt do menadżera. '''
        (textureId, img) = self.__sprite_name_to_texture(spriteName)
        self.__sprites[ spriteName ] = (textureId, spriteScript, float(img.width), float(img.height))

        
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
        ''' Zwraca klatkę do narysowania - obiekt typu SpriteAnimationFrame '''

        animation = self.__sprites[ spriteName ][ 1 ][ animationName ]
        
        texWidth  = self.__sprites[ spriteName ][ 2 ]
        texHeight = self.__sprites[ spriteName ][ 3 ]

        # oblicz współrzędne lewego dolnego rogu
        texLeft   = animation.x_offset + frameNum * animation.frame_width # pozycja, jeżeli pominiemy możliwość wielu wierszy na animację
        texBottom = animation.y_offset + (texLeft / (animation.cols_count * animation.frame_width)) * animation.frame_height
        texLeft  %= animation.cols_count * animation.frame_width

        # oblicz współrzędne prawego górnego rogu
        texRight  = texLeft + animation.frame_width
        texTop    = texBottom - animation.frame_height

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


    def check_sprite_collision(self, sprite1, sprite2, delta):
        ''' Sprawdza czy jeżeli na sprite1 nałożymy sprite2 w pozycji delta
        (jest to przesunięcie lewego dolnego rogu sprite2 względem lewego dolnego
        rogu sprite1), to czy istnieją dwa pikesele które nachodzą na siebie
        (czyli czy przecięcie miejsc gdzie oba nie mają kanału alfa 0 jest niepuste). '''
        return True
