from Checkmate import Checkmate
from socket import *
from Test import Test
from json import *

test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))

test.send(s1, '{"op":"start","params":["single","easy","None"]}')
test.send(s1, '{"op":"setdepth","params":[1]}')
test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'e2 e4'))
test.send(s1, '{"op":"save","params":[%s]}' % ('pgnfile',))

test.send(s1, '{"op":"history"}')
test.send(s1, '{"op":"quit"}')

s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

test.send(s2, '{"op":"start","params":["single","easy","None"]}')
test.send(s2, '{"op":"load","params":[%s]}' % ('pgnfile',))

test.send(s2, '{"op":"history"}')

test.send(s2, '{"op":"newgame"}')

test.send(s2, '{"op":"history"}')

test.send(s2, '{"op":"quit"}')
