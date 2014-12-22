from socket import *
from json import *

from Test import Test


test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))
s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

data = test.send(s1, '{"op":"start","params":["single","easy","None"]}')
data = loads(data)
gameid = data['gameid']

test.send(s1, '{"op":"play","params":["setdepth","1"]}')
test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'e2 e4'))

test.send(s1, '{"op":"exit"}')

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))

test.send(s1, '{"op":"connect" ,"gameid":"%d"}' % gameid)
test.send(s1, '{"op":"play","params":["getboard"]}')
test.send(s1, '{"op":"play","params":["history"]}')
test.send(s1, '{"op":"play","params":["changemode","multi"]}')

test.send(s2, '{"op":"connect","color":"Black","gameid":"%d"}' % gameid)

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'e4 e5'))

test.send(s2, '{"op":"play","params":["getboard"]}')
test.send(s2, '{"op":"play","params":["history"]}')
test.send(s2, '{"op":"exit"}')

s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

test.send(s2, '{"op":"connect","color":"Black","gameid":"%d"}' % gameid)
test.send(s2, '{"op":"play","params":["getboard"]}')
test.send(s2, '{"op":"play","params":["history"]}')

test.send(s2, '{"op":"kill"}')
test.send(s1, '{"op":"kill"}')