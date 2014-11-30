from threading import *
from socket import *
from Checkmate import *
from pickle import *
"""

start single hard /asd/qwe
start multi None /asd/qwe GAMEID
continue 5


save
exit

CM init single hard /asd/qwe GAMEID
CM init multi None None GAMEID



example:
load filename
history
setdepth depth

"""
GAMEID = 1

class Game(Checkmate):
	def __init__(self, mode="single", difficulty="hard", book=None):
		Checkmate.__init__(self)
		self.id = GAMEID
		GAMEID += 1



class Agent(Thread):
	def __init__(self,conn,addr,checkmateserver):
		Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.checkmateserver = checkmateserver

	def run(self):
		data = self.conn.recv(1024).strip().split()
		if data[0] == 'start':
			
			self.game = Game( data[1] , data[2] , data[3] )
		elif data[0] == 'continue':
			self.game = load( open(str(data[1]+'.p'),'rb') )
		self.checkmateserver.l.acquire()
		self.checkmateserver.games.append(self.game)
		self.checkmateserver.l.release()
		while True:
			data = self.conn.recv(1024).strip().split()

			if data[0] == 'exit':
				self.checkmateserver.l.acquire()
				self.checkmateserver.games.remove( self.game )
				self.checkmateserver.l.release()
				
				

class CheckmateServer():

	def __init__(self):
		sock = socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('0.0.0.0',20000))
		sock.listen(1)
		self.games = []
		self.l = Lock()
		while True:
			conn , addr =  sock.accept()
			agent = Agent(conn,addr,self)
			agent.start()

