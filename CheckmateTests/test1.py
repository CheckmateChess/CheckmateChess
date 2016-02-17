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


# Scholar's mate
from Checkmate import Checkmate
from Test import Test

a = Checkmate(mode='multi')

moves = [('White', 'e2 e4'), ('Black', 'a7 a6'), ('White', 'd1 f3'), ('Black', 'a6 a5'), ('White', 'f1 c4'),
         ('Black', 'a5 a4'), ('White', 'f3 f7')]

dummy = Test()

for move in moves:
    a.nextmove(move[0], move[1])
    dummy.show(a)

a.quit()
