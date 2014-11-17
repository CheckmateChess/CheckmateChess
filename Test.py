from Checkmate import Checkmate

class Test:

    def show(self,checkmate):
        print "#### SHOW ####"
        print 'Winner      : ', checkmate.getwinner()
        print 'Next Player : ', checkmate.currentplayer()
        print 'Finished    : ', checkmate.isfinished()
        print 'Mode        : ', checkmate.getmode()
        print 'Board       : '
        for row in checkmate.getboard():
            print '             ',
            for frame in row:
                print frame,
            print
        print "##############\n\n\n"

