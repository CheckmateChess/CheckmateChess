from random import randint

from Checkmate import Checkmate
from Test import Test


bookmodes = ['worst', 'best', 'random']

a = Checkmate(mode='multi')

# Be sure to download and extract http://ftp.gnu.org/gnu/chess/book_1.00.pgn.gz
a.addbook('book_1.00.pgn')
a.enablebook(enable=True)

dummy = Test()

while not a.isfinished():

    a.setbookmode(bookmodes[randint(0, 2)])

    move = a.hint()

    if move:
        a.nextmove(a.currentplayer(), move)
    else:
        break

    dummy.show(a)

a.quit()