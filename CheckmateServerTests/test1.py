from socket import *
from json import *

from Test import Test


moves = [('White', 'e2 e4'), ('Black', 'a7 a6'), ('White', 'd1 f3'), ('Black', 'a6 a5'), ('White', 'f1 c4'),
         ('Black', 'a5 a4'), ('White', 'f3 f7')]

test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))

s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

data = test.send(s1, '{"op":"start" , "color":"White","params":["multi","None","None"]}')

data = loads(data)
gameid = data['gameid']

test.send(s2, '{"op":"connect" , "color":"Black","gameid":"%d"}' % gameid)

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[0])
test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[1])
test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[2])
test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[3])
test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[4])
test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[5])
test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[6])

test.send(s2, '{"op":"kill"}')
test.send(s1, '{"op":"kill"}')
