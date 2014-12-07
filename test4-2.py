from socket import *

from Test import Test


test = Test()

s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

test.send(s2, '{"op":"connect", "color":"Black", "gameid":"%d"}' % 1)

test.send(s2, '{"op":"kill"}')
