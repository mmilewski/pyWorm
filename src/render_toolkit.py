#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyglet.gl import *


def draw_textured_quad( tex_coords, vertices, texture ):
    ''' Wyświetla czworokąt/sprite. '''

    glEnable( GL_TEXTURE_2D )
    assert glIsTexture( texture ), "Próba narysowania czegoś, co nie jest teksturą, jest %s" % type(texture)
    glBindTexture( GL_TEXTURE_2D, texture )
    glBegin( GL_QUADS )
    for t,v in zip(tex_coords,vertices):
        glTexCoord2f( *t )
        glVertex2f( *v )
    glEnd()
    glDisable( GL_TEXTURE_2D )

def compute_tex_vertex_coords( obj, frame, winWidth, winHeight ):
    ''' Zwraca parę (współrzędne tekstury, współrzędne wierzchołka) dla obiektu `obj` '''
    tex_left, tex_bottom, tex_right, tex_top = frame.rect
#         winWidth, winHeight = self.__theApp.get_window_dim()

    vertex_left, vertex_bottom = obj.position
    vertex_right = vertex_left + frame.width / float(winWidth)
    vertex_top = vertex_bottom + frame.height / float(winHeight)

    tc = ( (tex_left, tex_bottom), (tex_right, tex_bottom), (tex_right, tex_top), (tex_left, tex_top) )
    vs = ( (vertex_left, vertex_bottom), (vertex_right, vertex_bottom), (vertex_right, vertex_top), (vertex_left, vertex_top) )

    return (tc,vs)
