from Checkmate import Checkmate
from Test import Test

a = Checkmate(mode='multi')
print a.nextmove('White', 'e4')

dummy = Test()
dummy.show(a)

print a.nextmove('Black', 'a6')
print a.nextmove('White', 'd1 f3')
print a.nextmove('Black', 'a5')
print a.nextmove('White', 'f1 c4')
print a.nextmove('Black', 'a4')
print a.nextmove('White', 'f3 f7')
print a.isfinished()
print a.winner
a.quit()