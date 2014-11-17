class Test:
    def show(self, checkmate):
        print "#### SHOW ####"
        print 'Finished    : ', checkmate.isfinished()
        print 'Winner      : ', checkmate.getwinner()
        print 'Next Player : ', checkmate.currentplayer()
        print 'Mode        : ', checkmate.getmode()
        print 'Book mode   : ', checkmate.getbookmode()
        print 'History     : ', checkmate.history()
        print 'Board       : '
        for row in checkmate.getboard():
            print '             ',
            for frame in row:
                print frame,
            print
        print "##############\n\n\n"

