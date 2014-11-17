from Checkmate import Checkmate

class Test:

    def show(self,checkmate):
        print "#### SHOW ####"
        print 'Winner      : ', checkmate.winner
        print 'Next Player : ', checkmate.nextplayer
        print 'Finished    : ', checkmate.finished
        print 'Mode        : ', checkmate.mode
        print 'Board       : '
        for row in checkmate.board:
            for frame in row:
                print frame,
            print
        print "##############\n\n\n"

