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


from subprocess import Popen, PIPE
from os.path import isfile
from time import sleep


class Checkmate:
    """
    Checkmate is a python class interface for GNUChess.
    """

    def __init__(self, mode="single", difficulty="hard", book=None):
        """
        Creates a GNUChess process and makes necessary configurations of I/O streams.
        @param mode: string, single|multi
        @param difficulty: string, hard|easy
        @param book: string|None, absolute path of the book file
        @return: Checkmate instance
        """
        self.mode = mode
        self.winner = None
        self.finished = False
        self.nextplayer = None
        self.board = None
        self.depth = None
        self.bookmode = None
        self.command = ['/usr/games/gnuchess', '-q']
        if mode == 'multi':
            self.command.append('-m')
        if difficulty == 'easy':
            self.command.append('-e')
        if book is not None and isfile(book):
            self.command.extend(['-a', book])
        self.process = Popen(self.command, stdin=PIPE, stdout=PIPE)
        self.readgarbage(1)
        self.readnextplayer()
        self.process.stdin.write('show board\n')
        self.readgarbage(4)
        self.readboard()
        self.readgarbage(1)

    def nextmove(self, side, move):
        """
        Make next move.
        @param side: string, black|white
        @param move: string, [a-h][1-8] [a-h][1-8]
        @return: bool, True|False, whether move is valid.
        """
        if self.nextplayer != side:
            return False
        self.process.stdin.write('%s\n' % move)
        self.readgarbage(2)
        if self.process.stdout.readline() == "Invalid move: %s\n" % move:
            return False
        self.readgarbage(2)
        self.readboard()
        self.readgarbage(1)
        if self.mode == 'multi':
            self.readnextplayer()
        else:
            self.readgarbage(2)
            newline = self.process.stdout.readline()
            if newline.find('TimeLimit') != -1:
                self.readgarbage(3)
            self.readboard()
            self.readgarbage(3)
            self.readnextplayer()
        self.process.stdin.write('\n')
        line = self.process.stdout.readline()

        if '{' in line:
            self.readgarbage(3)
            self.finished = True
            self.winner = line[line.find('{') + 1:][:5]
        else:
            self.readgarbage(2)
        return True

    def save(self, filename):
        """
        Saves current game state to file.
        @param filename: absolute path of the file.
        @return: bool, True|False, whether it is saved successfully.
        """
        if filename is None:
            return False
        self.process.stdin.write('pgnsave %s\n' % filename)
        self.readgarbage(2)
        return True

    def load(self, filename):
        """
        Loads current game state from file.
        @param filename: absolute path of the file.
        @return: bool, True|False, whether it is loaded successfully.
        """
        if filename is None or not isfile(filename):
            return False
        self.process.stdin.write('pgnload %s\n' % filename)
        self.readgarbage(4)
        self.readboard()
        self.readgarbage(1)
        self.readnextplayer()
        return True

    def hint(self):
        """
        Gives hint as a move.
        @return: string, [a-h][1-8] [a-h][1-8]
        """
        hint = None
        self.process.stdin.write('hint\n')
        self.readgarbage(2)
        sleep(0.5)
        self.process.stdin.write('\n')
        line = self.process.stdout.readline()
        if line.find('Hint:') != -1:
            hint = line[line.find('Hint:') + 6: -1]
            self.readgarbage(3)
        else:
            self.readgarbage(2)
        return hint

    def addbook(self, filename):
        """
        Compiles the given file.
        @param filename: string, absolute path of the file
        @return: bool, True|False, whether it is added successfully.
        """
        if filename is None or not isfile(filename):
            return False
        self.process.stdin.write('book add %s\n' % filename)
        while self.process.stdout.readline() != 'all done!\n':
            pass
        return True

    def enablebook(self, enable=True):
        """
        Enables or disables book.
        @param enable: bool, True|False
        @return: bool, True|False, whether operation is successful
        """
        if enable:
            self.process.stdin.write('book on\n')
        else:
            self.process.stdin.write('book off\n')
        self.readgarbage(3)
        return True

    def setbookmode(self, mode):
        """
        Changes move preference from book.
        @param mode: string, worst|best|random
        @return: bool, True|False, whether operation is successful
        """
        if mode not in ['worst', 'best', 'random']:
            return False
        self.bookmode = mode
        self.process.stdin.write('book %s\n' % mode)
        self.readgarbage(3)
        return True

    def getboard(self):
        """
        Returns current game board.
        @return: list of lists, each row is a list, list of rows
        """
        # self.process.stdin.write('show board\n')
        #self.readgarbage(4)
        #self.readboard()
        #self.readgarbage(1)
        return self.board

    def history(self):
        """
        Returns all made move history.
        @return: dictionary of lists, lists contain moves
        """
        history = {
            'White': [],
            'Black': [],
        }
        self.process.stdin.write('show game\n')
        self.readgarbage(2)
        if self.process.stdout.read(1) != ' ':
            return history
        sides = [i for i in self.process.stdout.readline().strip().split() if i != '']
        while 1:
            line = self.process.stdout.readline()
            if line == '\n':
                break
            moves = [i for i in line[6:].strip().split(' ') if i != '']
            for i in range(2):
                if i < len(moves):
                    history[sides[i]].append(moves[i])
        return history

    def quit(self):
        """
        Exits game.
        """
        self.process.stdin.write('quit\n')
        self.process.wait()

    def isfinished(self):
        """
        Checks whether game is finished.
        @return: bool, True|False
        """
        return self.finished

    def getwinner(self):
        return self.winner

    def undo(self):
        """
        Backs up one move in game history.
        @return: bool, True|False, whether operation is successful
        """
        if self.mode == 'single':
            return False
        success = True
        self.process.stdin.write('undo\n')
        self.readgarbage(2)
        if self.process.stdout.readline() == 'No moves to undo!\n':
            success = False
            self.readgarbage(2)
        else:
            self.readgarbage(1)
        self.readboard()
        self.readgarbage(1)
        self.readnextplayer()
        return success

    def setdepth(self, depth=0):
        """
        Sets the program to look depth moves deep for every search it performs.
        @depth: int
        """
        self.depth = depth
        self.process.stdin.write('depth %d\n' % depth)
        self.readgarbage(3)

    def getdepth(self):
        """
        @return: returns depth
        """
        return self.depth

    def getbookmode(self):
        """
        @return: returns bookmode
        """
        return self.bookmode

    def newgame(self):
        """
        Sets up a new game.
        """
        self.process.stdin.write('new\n')
        self.readgarbage(2)
        self.readnextplayer()
        self.process.stdin.write('show board\n')
        self.readgarbage(4)
        self.readboard()
        self.readgarbage(1)

    def changemode(self, mode):
        """
        Changes game mode.
        @param mode: string, single|manual
        @return: bool, whether operation is successful
        """
        if self.mode == mode:
            return False
        self.mode = mode
        if mode == 'multi':
            self.process.stdin.write('manual\n')
            self.readgarbage(2)
            self.readnextplayer()
        else:
            self.process.stdin.write('go\n')
            self.readgarbage(5)
            self.readboard()
            self.readgarbage(3)
            self.readnextplayer()
        return True

    def getmode(self):
        """
        @return: returns game mode
        """
        return self.mode

    def currentplayer(self):
        """
        Returns who will make the next move.
        @return: string, Black|White
        """
        return self.nextplayer

    def readgarbage(self, count):
        """
        reads garbage lines
        """
        for i in range(count):
            self.process.stdout.readline()

    def readnextplayer(self):
        """
        reads next player and stores in self.nextplayer
        """
        self.process.stdin.write('\n')
        line = self.process.stdout.readline()
        self.nextplayer = line[:5]
        if '{' in line:
            self.finished = True
            self.winner = line[line.find('{') + 1:][:5]
        self.readgarbage(2)

    def readboard(self):
        """
        reads current board
        """
        self.board = []
        for i in range(8):
            self.board.append(self.process.stdout.readline().strip().split(' '))
