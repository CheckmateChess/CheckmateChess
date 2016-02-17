# This file is part of Checkmate. 
# 
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Copyright 2015 Ozge Lule(ozge.lule@ceng.metu.edu.tr), 
#                Esref Ozturk(esref.ozturk@ceng.metu.edu.tr)


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
