from subprocess import Popen, PIPE
from os.path import isfile


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
        self.command = ['/usr/games/gnuchess','-q']
        if mode == 'multi':
            self.command.append('-m')
        if difficulty == 'easy':
            self.command.append('-e')
        if book is not None and isfile(book):
            self.command.extend(['-a', book])
        self.process = Popen(self.command, stdin=PIPE, stdout=PIPE)
        self.readgarbage(1)
        self.readnextplayer()
        self.mode = mode
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

    def save(self, filename):
        """
        Saves current game state to file.
        @param filename: absolute path of the file.
        @return: bool, True|False, whether it is saved successfully.
        """

    def load(self, filename):
        """
        Loads current game state from file.
        @param filename: absolute path of the file.
        @return: bool, True|False, whether it is loaded successfully.
        """

    def hint(self):
        """
        Gives hint as a move.
        @return: string, [a-h][1-8] [a-h][1-8]
        """

    def addbook(self, filename):
        """
        Compiles the given file.
        @param filename: string, absolute path of the file
        @return: bool, True|False, whether it is added successfully.
        """

    def enablebook(self, enable=True):
        """
        Enables or disables book.
        @param enable: bool, True|False
        @return: bool, True|False, whether operation is successful
        """

    def bookmode(self, mode):
        """
        Changes move preference from book.
        @param mode: string, worst|best|random
        @return: bool, True|False, whether operation is successful
        """

    def board(self):
        """
        Returns current game board.
        @return: list of lists, each row is a list, list of rows
        """
        return self.board

    def history(self):
        """
        Returns all made move history.
        @return: dictionary of lists, lists contain moves
        """

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

    def undo(self):
        """
        Backs up one move in game history.
        @return: bool, True|False, whether operation is successful
        """

    def setdepth(self, depth=0):
        """
        Sets the program to look depth moves deep for every search it performs.
        @depth: int
        @return: bool, whether operation is successful
        """
        self.process.stdin.write('depth %d\n' % depth)
        self.readgarbage(3)

    def newgame(self):
        """
        Sets up a new game.
        """
        self.process.stdin.write('new\n')
        self.readgarbage(2)
        self.readnextplayer()

    def changemode(self, mode):
        """
        Changes game mode.
        @param mode: string, single|manual
        @return: bool, whether operation is successful
        """
        if self.mode == mode:
            return False
        self.mode = mode
        if mode == 'single':
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

    def currentplayer(self):
        """
        Returns who will make the next move.
        @return: string, Black|White
        """
        return self.nextplayer

    def readgarbage(self,count):
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
        self.nextplayer = self.process.stdout.readline()[:5]
        self.readgarbage(2)
        print self.nextplayer

    def readboard(self):
        """
        reads current board
        """
        self.board = []
        for i in range(8):
            self.board.append(self.process.stdout.readline().strip().split(' '))
        print self.board