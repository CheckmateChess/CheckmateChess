class Checkmate:
	'''
	Checkmate is a python class interface for GNUChess.
	'''
	
	def __init__(self, mode="single", difficulty="hard", book=None):
		'''
		Creates a GNUChess process and makes necessary configurations of I/O streams.
		@param mode: string, single|multi
		@param difficulty: string, hard|easy
		@param book: string|None, absolute path of the book file
		@return: Checkmate instance
		'''
	
	def nextmove(self, side, move):
		'''
		make next move.
		@param side: string, black|white
		@param move: string, [a-h][1-8] [a-h][1-8]
		@return: bool, True|False, whether move is valid.
		'''
	
	def save(self, filename):
		'''
		saves current game state to file.
		@param filename: absolute path of the file.
		@return: bool, True|False, whether it is saved successfully.
		'''
	
	def load(self, filename):
		'''
		loads current game state from file.
		@param filename: absolute path of the file.
		@return: bool, True|False, whether it is loaded successfully.
		'''
	
	def hint(self):
		'''
		gives hint as a move.
		@return: string, [a-h][1-8] [a-h][1-8]
		'''
	
	def addbook(self, filename):
		'''
		compiles the given file.
		@param filename: string, absolute path of the file
		@return: bool, True|False, whether it is added successfully.
		'''
	
	def enablebook(self, enable=True):
		'''
		enables or disables book.
		@param enable: bool, True|False
		@return: bool, True|False, whether operation is successful
		'''
	
	def bookmode(self, mode):
		'''
		changes move preference from book.
		@param mode: string, worst|best|random
		@return: bool, True|False, whether operation is successful
		'''
	
	def board(self):
		'''
		returns current game board.
		@return: list of strings, each row is a string, list of rows 
		'''
	
	def history(self):
		'''
		returns all moves.
		@return: dictionary of lists, lists contain moves
		'''
	
	def quit(self):
		'''
		exits game.
		'''
	
	def isfinished(self):
		'''
		checks whether game is finished.
		@return: bool, True|False
		'''
	
	def undo(self):
		'''
		backs up one move in game history.
		@return: bool, True|False, whether operation is successful
		'''
	def setdepth(self, depth=0):
		'''
		Sets the program to look depth moves deep for every search it performs.
		@depth: int
		@return: whether operation is successful
		'''





