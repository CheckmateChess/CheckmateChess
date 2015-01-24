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


from socket import *

from Test import Test


moves = [('Black', 'a7 a6'), ('Black', 'a6 a5'), ('Black', 'a5 a4')]

test = Test()

s2 = socket(AF_INET, SOCK_STREAM)
s2.connect(("0.0.0.0", 20000))

gameid = 1

test.send(s2, '{"op":"connect" , "color":"Black","gameid":"%d"}' % gameid)

test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[0])

test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[1])

test.send(s2, '{"op":"play","params":["nextmove","%s","%s"]}' % moves[2])

test.send(s2, '{"op":"kill"}')