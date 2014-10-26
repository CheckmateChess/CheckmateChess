class Checkmate:
	'''
	Checkmate is a python class interface for GNUChess.
	'''
	def __init__(self, mode="single", difficulty=):
		'''
		Creates a GNUChess process and makes necessary configurations of I/O streams.
		@param mode: string, single|multi
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
