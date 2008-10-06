#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../src")

from spriteScriptParser import SpriteScriptParser

parser = SpriteScriptParser("test_sprite")
parser.parse()

logic  = parser.get_logic_part()
sprite = parser.get_sprite_part()

failed_count = 0

def test(value, correctValue, description):
    print description + ": ",
    if value == correctValue:
        print "OK"
        return 0
    else:
        print "FAILED: should be", correctValue, "got", value
        return 1

failed_count += test(logic['leci'].duration, 100, "leci.duration")
failed_count += test(logic['leci'].frames_count, 7, "leci.frames_count")
failed_count += test(sprite['leci'].y_offset, 0, "leci.y_offset")
failed_count += test(sprite['leci'].x_offset, 0, "leci.x_offset")
failed_count += test(sprite['leci'].frame_width, 130, "leci.frame_width")
failed_count += test(sprite['leci'].frame_height, 90, "leci.frame_height")
failed_count += test(sprite['leci'].cols_count, 7, "leci.cols_count")

print
failed_count += test(logic['pochyla sie przod'].duration, 50, 'pochyla sie przod.duration')
failed_count += test(logic['pochyla sie przod'].frames_count, 3, 'pochyla sie przod.frames')
failed_count += test(sprite['pochyla sie przod'].y_offset, 90, 'pochyla sie przod.y_offset')
failed_count += test(sprite['pochyla sie przod'].x_offset, 0, 'pochyla sie przod.x_offset')
failed_count += test(sprite['pochyla sie przod'].frame_width, 130, 'pochyla sie przod.frame')
failed_count += test(sprite['pochyla sie przod'].frame_height, 90, 'pochyla sie przod.frame')
failed_count += test(sprite['pochyla sie przod'].cols_count, 3, 'pochyla sie przod.cols')

print
failed_count += test(logic['leci przod pochylony'].duration, 100, 'leci przod pochylony.duration')
failed_count += test(logic['leci przod pochylony'].frames_count, 7, 'leci przod pochylony.frames')
failed_count += test(sprite['leci przod pochylony'].y_offset, 180, 'leci przod pochylony.y_offset')
failed_count += test(sprite['leci przod pochylony'].x_offset, 0, 'leci przod pochylony.x_offset')
failed_count += test(sprite['leci przod pochylony'].frame_width, 130, 'leci przod pochylony.frame')
failed_count += test(sprite['leci przod pochylony'].frame_height, 90, 'leci przod pochylony.frame')
failed_count += test(sprite['leci przod pochylony'].cols_count, 7, 'leci przod pochylony.cols')

print
failed_count += test(logic['pochyla sie tyl'].duration, 50, 'pochyla sie tyl.duration')
failed_count += test(logic['pochyla sie tyl'].frames_count, 3, 'pochyla sie tyl.frames')
failed_count += test(sprite['pochyla sie tyl'].y_offset, 270, 'pochyla sie tyl.y_offset')
failed_count += test(sprite['pochyla sie tyl'].x_offset, 0, 'pochyla sie tyl.x_offset')
failed_count += test(sprite['pochyla sie tyl'].frame_width, 130, 'pochyla sie tyl.frame')
failed_count += test(sprite['pochyla sie tyl'].frame_height, 90, 'pochyla sie tyl.frame')
failed_count += test(sprite['pochyla sie tyl'].cols_count, 3, 'pochyla sie tyl.cols')
      
print
failed_count += test(logic['leci tyl pochylony'].duration, 100, 'leci tyl pochylony.duration')
failed_count += test(logic['leci tyl pochylony'].frames_count, 7, 'leci tyl pochylony.frames')
failed_count += test(sprite['leci tyl pochylony'].y_offset, 360, 'leci tyl pochylony.y_offset')
failed_count += test(sprite['leci tyl pochylony'].x_offset, 0, 'leci tyl pochylony.x_offset')
failed_count += test(sprite['leci tyl pochylony'].frame_width, 130, 'leci tyl pochylony.frame')
failed_count += test(sprite['leci tyl pochylony'].frame_height, 90, 'leci tyl pochylony.frame')
failed_count += test(sprite['leci tyl pochylony'].cols_count, 7,  'leci tyl pochylony.cols')

print
if failed_count != 0:
    print failed_count, "tests failed"
    exit(1)
else:
    print "all test passed"
    exit(0)
    
