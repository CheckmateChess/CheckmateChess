from random import randint
from socket import *
from json import *

from Test import Test

bookmodes = ['worst', 'best', 'random']

test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))

s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

data = test.send(s1, '{"op":"start", "color":"White","params":["multi","None","None"]}')

data = loads(data)
gameid = data['gameid']

test.send(s2, '{"op":"connect" , "color":"Black","gameid":"%d"}' % gameid)

# Be sure to download and extract http://ftp.gnu.org/gnu/chess/book_1.00.pgn.gz

test.send(s1, '{"op":"play","params":["addbook","book_1.00.pgn"]}')
test.send(s1, '{"op":"play","params":["enablebook","True"]}')

count = 0
while True:

    if count % 2 == 0:
        test.send(s1, '{"op":"play","params":["setbookmode","%s"]}' % bookmodes[randint(0, 2)])
        move = test.send(s1, '{"op":"play","params":["hint"]}')
        move = loads(move)
        if move['hint']:
            test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ("White", move['hint']))
        else:
            test.send(s1, '{"op":"kill"}')
            test.send(s2, '{"op":"kill"}')
            exit(1)

        data2 = test.send(s2, '{"op":"play","params":["isfinished"]}')
        data2 = loads(data2)

        if data2['isfinished']:
            test.send(s2, '{"op":"kill"}')
            test.send(s1, '{"op":"kill"}')

            exit()
    else:
        test.send(s2, '{"op":"play","params":["setbookmode","%s"]}' % bookmodes[randint(0, 2)])
        move = test.send(s2, '{"op":"play","params":["hint"]}')
        move = loads(move)
        if move['hint']:
            test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % ("Black", move['hint']))
        else:
            test.send(s2, '{"op":"kill"}')
            test.send(s1, '{"op":"kill"}')

            exit()

        data1 = test.send(s1, '{"op":"play","params":["isfinished"]}')
        data1 = loads(data1)

        if data1['isfinished']:
            test.send(s1, '{"op":"kill"}')
            test.send(s2, '{"op":"kill"}')

            exit()

    count += 1