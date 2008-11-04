#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../src")

import levelParser as LP

p = LP.LevelScriptParser('levelParser.input')
b = p.parse()

print '\nStatus parsowania:', 'SUKCES' if b else 'PORAŻKA'
