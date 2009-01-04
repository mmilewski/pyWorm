#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../src")

import levelParser as LP


p = LP.LevelParser('levelParser.input')

print "\nWczytano poziom. Oto nazwa i autor:\n-----------------------------------"
print "Level name:", p.get_level_name(), "\nAuthor:", p.get_level_author()

print "\nTestowanie menedżera akcji\n--------------------------"
am = p.get_action_manager()
am.perform_up_to(1000)

print "\nTestowanie menedżera podłoża\n--------------------------"
gm = p.get_ground_manager()
print gm.get_grounds()
