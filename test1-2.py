from Checkmate import Checkmate
from socket import *
from Test import Test
from json import *

moves = [('Black', 'a7 a6'), ('Black', 'a6 a5'),('Black', 'a5 a4')]

test = Test()

s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

gameid = 1

test.send(s2, '{"op":"connect" , "color":"Black","gameid":"%d"}' % gameid)


test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[0])

test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[1])

test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[2])


s2.shutdown(SHUT_RDWR)
s2.close()