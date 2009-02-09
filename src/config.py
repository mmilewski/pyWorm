#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Moduł zawiera różne opcje konfiguracyjne.'''

# True - program zostanie uruchomiony na pełnym ekranie, False - w oknie.
IS_FULLSCREEN = False

# rozmiar okna, jeżeli program jest uruchamiany w oknie. Inaczej jest bez znaczenia.
WIN_SIZE = (800,600)

# True - zostanie włączona synchronizacja pionowa, False - bez synchronizacji.
IS_VSYNC = True

# True - obraz będzie najpierw renderowany do tekstury, False - od razu na ekran.
IS_RENDER_TO_TEXTURE = False

# True - wyświetlanie nie przekroczy FPS_LIMIT klatek na sekundę.
IS_FPS_LIMIT = False

# patrz IS_FPS_LIMIT.
FPS_LIMIT = 50

# czy wypisywać FPSy (na konsolę)
PRINT_FPS = False

# prędkość przewijania się obiektów na scenie.
SCROLL_VELOCITY_OBJECT = (-0.11,0)

# poziom, po którym poruszają się pojazdy naziemne. Zwiększenie, nie spowoduje, że
# podłoże będzie rysowane wyżej, tylko że obiekty będą fruwały w powietrzu.
GROUND_LINE = 0.25

# czas wyświetlania ekranu splash (w sekundach).
SPLASH_DISPLAY_TIME = .5

# współrzynnik, przez który będzie mierzony upływ czasu. Jeśli >1, to gra przyspieszy
DTIME_MULTIPLY = 1.0
