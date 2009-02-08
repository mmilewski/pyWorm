#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Moduł zawiera różne opcje konfiguracyjne.'''

# True - program zostanie uruchomiony na pełnym ekranie, False - w oknie
IS_FULLSCREEN = False

# współrzędne okna, jeżeli program jest uruchamiany w oknie
WIN_SIZE = (800,600)

# True - zostanie włączona synchronizacja pionowa, False - bez synchronizacji
IS_VSYNC = True

# True - obraz będzie najpierw renderowany do tekstury, False - od razu na ekran.
IS_RENDER_TO_TEXTURE = False

# True - wyświetlanie nie przekroczy FPS_LIMIT klatek na sekundę,
IS_FPS_LIMIT = False

# patrz IS_FPS_LIMIT
FPS_LIMIT = 50

# prędkość przewijania się obiektów na scenie
SCROLL_VELOCITY_OBJECT = (-0.11,0)

# poziom, po którym poruszają się pojazdy naziemne
GROUND_LINE = 0.25

# czas wyświetlania ekranu splash
SPLASH_DISPLAY_TIME = 3
