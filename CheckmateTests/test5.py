from Checkmate import Checkmate
from Test import Test

a = Checkmate(mode='multi')
dummy = Test()

a.setdepth(1)

a.nextmove('White', 'e2 e4')

dummy.show(a)

a.changemode('single')

dummy.show(a)

a.changemode('multi')

dummy.show(a)

if not a.nextmove('White', 'asdf'):
    print 'Invalid move!', '\n'

dummy.show(a)

a.quit()