from Checkmate import Checkmate
from Test import Test

a = Checkmate(mode='multi')
a.addbook('book_1.00.pgn')
a.enablebook(enable=True)

dummy = Test()

while not a.isfinished():
    print '------------------------------------------------------ girdim '
    move = a.hint()
    print '------------------------------------------------------ hinti aldim '
    print move
    print '------------------------------------------------------'

    if move:
        a.nextmove(a.currentplayer(), move)
    else:
        break
    print '------------------------------------------------------ oynadim '
    dummy.show(a)

a.quit()