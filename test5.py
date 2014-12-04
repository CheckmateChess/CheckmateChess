from Checkmate import Checkmate
from socket import *
from Test import Test
from json import *

test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))

test.send(s1, '{"op":"start","params":["multi","None","None"]}')
test.send(s1, '{"op":"setdepth","params":[%d]}' % (1,))

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'e2 e4'))

board = test.send(s1, '{"op":"getboard"}')

test.send(s1, '{"op":"changemode","params":[%s]}' % ('single',))

board = test.send(s1, '{"op":"getboard"}')

test.send(s1, '{"op":"changemode","params":[%s]}' % ('multi',))

board = test.send(s1, '{"op":"getboard"}')

nextmove = test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'afdsaf'))

nextmove = loads(nextmove)

if not nextmove['success']:
    print 'Invalid move!', '\n'

board = test.send(s1, '{"op":"getboard"}')

test.send(s1, '{"op":"quit"}')
