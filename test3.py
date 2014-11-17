from Checkmate import Checkmate

a = Checkmate(difficulty='easy')
a.setdepth(1)
a.nextmove('White', 'e2 e4')
a.save('pgnfile')
print a.history()
a.quit()

b = Checkmate()
b.load('pgnfile')
print b.history()
b.quit()