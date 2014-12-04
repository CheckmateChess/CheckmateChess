from random import randint

from Checkmate import Checkmate
from Test import Test
from socket import *
from json import *

bookmodes = ['worst', 'best', 'random']

test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))

s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

data = test.send(s1, '{"op":"start","params":["multi","None","None"]}')

data = loads(data)
gameid = data['gameid']

test.send(s2, '{"op":"connect","gameid":"%d"}' % gameid)

# Be sure to download and extract http://ftp.gnu.org/gnu/chess/book_1.00.pgn.gz

test.send(s1, '{"op":"addbook","params":"book_1.00.pgn"}')
test.send(s1, '{"op":"enablebook","params":"True"}')

count = 0
while True:

    data1 = test.send(s1, '{"op":"isfinished"}')
    data1 = loads(data1)

    if data1['isfinished']:
        break

    test.send(s1, '{"op":"setbookmode","params":"%s"}' % bookmodes[randint(0, 2)])

    if count % 2 == 0:
        move = test.send(s1, '{"op":"hint"}')
        move = loads(move)
        if move:
            test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ("White", move['hint']))
        else:
            break
    else:
        move = test.send(s2, '{"op":"hint"}')
        move = loads(move)
        if move:
            test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % ("Black", move['hint']))
        else:
            break

    count += 1

board = test.send(s1, '{"op":"getboard"}')
board = loads(board)

