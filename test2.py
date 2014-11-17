from random import randint

from Checkmate import Checkmate
from Test import Test


bookmodes = ['worst', 'best', 'random']

a = Checkmate(mode='multi')
a.addbook('book_1.00.pgn')
a.enablebook(enable=True)

dummy = Test()
# print '-------------------------------------------------------- basliyorum'
while not a.isfinished():
    #print '-------------------------------------------------------- girdim'
    a.setbookmode(bookmodes[randint(0, 2)])

    move = a.hint()
    #print '-------------------------------------------------------- hint aldim',move
    if move:
        a.nextmove(a.currentplayer(), move)
    else:
        break

    #print '-------------------------------------------------------- oynadim'

    dummy.show(a)

a.quit()