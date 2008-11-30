#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../src")

import levelParser as LP

p = LP.LevelParser('levelParser.input')
print "\nLevel name:",p.get_level_name(), "\nAuthor:",p.get_level_author()
