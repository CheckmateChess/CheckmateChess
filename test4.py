from Checkmate import Checkmate
from socket import *
from Test import Test
from json import *

test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))
s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

data = test.send(s1, '{"op":"start","color":"White","params":["multi","None","None"]}')

data = loads(data)
gameid = data['gameid']

test.send(s2, '{"op":"connect","color":"Black","gameid":"%d"}' % gameid)

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'e2 e4'))
test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % ('Black', 'a7 a6'))

test.send(s2, '{"op":"play","params":["undo"]}')
test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % ('Black', 'a7 a5'))

board = test.send(s2, '{"op":"getboard"}')

test.send(s2, '{"op":"exit"}')
