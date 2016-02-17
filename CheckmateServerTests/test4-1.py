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
from json import *
from Test import Test

test = Test()

s1 = socket(AF_INET, SOCK_STREAM)
s1.connect(("0.0.0.0", 20000))

data = test.send(s1, '{"op":"start","params":["single","None","None"]}')

data = loads(data)
gameid = data['gameid']

print gameid

test.send(s1, '{"op":"play","params":["setdepth",%d]}' % (1,))
test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'e2 e4'))

test.send(s1, '{"op":"play","params":["changemode","%s"]}' % ('multi',))

nextmove = test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'afdsaf'))

nextmove = loads(nextmove)

if not nextmove['success']:
    print 'Invalid move!', '\n'

test.send(s1, '{"op":"play","params":["getboard"]}')

test.send(s1, '{"op":"play","params":["nextmove","%s","%s"]}' % ('White', 'a4'))

test.send(s1, '{"op":"kill"}')
