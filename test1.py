#Scholar's mate
from Checkmate import Checkmate
from Test import Test

a = Checkmate(mode='multi')

moves = [ ('White','e2 e4') ,('Black', 'a7 a6') ,('White', 'd1 f3') ,('Black', 'a6 a5') ,('White', 'f1 c4') ,('Black', 'a5 a4'),('White', 'f3 f7')]

dummy = Test()

for move in moves:
    a.nextmove(move[0],move[1])
    dummy.show(a)

a.quit()