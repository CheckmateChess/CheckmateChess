from threading import *
from socket import *
from Checkmate import *

"""
example:
load filename
history
setdepth depth

"""
class Play():



class Agent(Thread):
	def __init__(self,conn,addr):
		Thread.__init__(self)
		self.conn = conn
		self.addr = addr

	def run(self):
		data = self.conn.recv(1024).strip().split()
		while True:
			if len(data) == 4 and data[0] == 'init':
				self.checkmate = Checkmate( data[1] , data[2] , data[3] )
				break
			else:
				self.conn.send('init <mode> <difficulty> <book> format expected\n')
		while True:
			data = self.conn.recv(1024).strip().split()
			pass
			#if data[0] == 'nextmove':	
				
				

class CheckmateServer():

	def __init__(self):
		sock = socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('0.0.0.0',20000))
		sock.listen(1)
		while True:
			conn , addr =  sock.accept()
			agent = Agent(conn,addr)
			agent.start()

