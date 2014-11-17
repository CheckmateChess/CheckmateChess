from Checkmate import Checkmate
from Test import Test

dummy = Test()

a = Checkmate(mode='multi')

a.nextmove('White', 'e2 e4')
a.nextmove('Black', 'a7 a6')

dummy.show(a)
print a.history(), '\n\n\n\n'

a.undo()

a.nextmove('Black', 'a7 a5')

dummy.show(a)
print a.history(), '\n\n\n\n'

a.quit()