#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet.gl import *
# class Hud(object):

#     def __init__(self, winSize):
#         self.__winSize = winSize
#         self.__fonts = { 'mono': font.load('Mono', 20) }

#     width = property(lambda self: self.__winSize[0])
#     height = property(lambda self: self.__winSize[1])

#     def update(self, dt):
#         # aktualizuj hud
#         # ...
#         pass

#     def draw(self):
#         self.text = font.Text(
#             self.__fonts['mono'],
#             ("%.1f" % clock.get_fps() ),
#             x = self.width / 2,
#             y = 0,
#             halign = font.Text.CENTER,
#             valign = font.Text.BOTTOM,
#             color  = (1, 1, 1, 1),
#         )
#         glMatrixMode(GL_MODELVIEW);
#         glLoadIdentity();
#         self.text.draw()
