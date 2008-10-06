#!/usr/bin/python
# -*- coding: utf-8 -*-

class AIStrategy(object):
    
    def update(self, dt): abstract
    ''' Metoda uaktualniająca stan obiektu.
        dt: czas jaki upłynął od ostatniego uruchomienia tej metody '''
