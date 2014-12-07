from socket import *

from Test import Test


moves = [('White', 'e2 e4'), ('White', 'd1 f3'), ('White', 'f1 c4'), ('White', 'f3 f7')]

test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))

test.send(s1, '{"op":"start" , "color":"White","params":["multi","None","None"]}')

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[0])

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[1])

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[2])

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[3])

test.send(s1, '{"op":"kill"}')