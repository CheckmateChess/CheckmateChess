from Checkmate import Checkmate
from socket import *
from Test import Test
from json import *

test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20001))

data = test.send(s1, '{"op":"start","params":["single","None","None"]}')

data = loads(data)
gameid = data['gameid']

print gameid

test.send(s1, '{"op":"play","params":["setdepth",%d]}' % (1,))
test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'e2 e4'))

test.send(s1, '{"op":"play","params":["changemode","%s"]}' % ('multi',))

nextmove = test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'afdsaf'))

nextmove = loads(nextmove)

if not nextmove['success']:
    print 'Invalid move!', '\n'

test.send(s1, '{"op":"play","params":["getboard"]}')

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'a4'))


