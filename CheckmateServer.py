from threading import *
from socket import *
from Checkmate import *
from json import *
"""

start single hard /asd/qwe
start multi None /asd/qwe
connect GAMEID
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
    def __init__(self, params):
        Checkmate.__init__(self, params[0], params[1], params[2])
        self.id = GAMEID
        self.lock = Lock()
        GAMEID += 1
        self.active = 1

        if params[0] == 'single':
            self.capacity = 1
        elif params[0] == 'multi':
            self.capacity = 2




class Agent(Thread):
    def __init__(self, conn,addr,checkmateserver):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.checkmateserver = checkmateserver

    def run(self):
        data = loads(self.conn.recv(1024).strip())

        if data['op'] == 'start':
            self.game = Game(data['params'])

            self.conn.send('Game created with id: {}'.format(self.game.id))

        elif data['op'] == 'connect':
            self.checkmateserver.l.acquire()
            game = self.checkmateserver.games[int(data['gameid'])]
            self.checkmateserver.l.release()

            if game.capacity - game.active > 0:
                game.lock.acquire()
                game.active += 1
                game.lock.release()
                self.game = game

        self.checkmateserver.l.acquire()
        self.checkmateserver.games[self.game.id] = self.game
        self.checkmateserver.l.release()



        while True:
            data = loads(self.conn.recv(1024).strip())

            if data['op'] == 'exit':
                self.game.lock.acquire()
                self.game.active -= 1
                self.game.lock.release()
                self.conn.close()
                return
            elif data['op'] == 'kill':
                self.checkmateserver.l.acquire()
                game = self.checkmateserver.games[data['gameid']]
                #TODO quit gonder
                del self.checkmateserver.games[data['gameid']]
                self.checkmateserver.l.release()
                self.conn.close()
                return

            elif data['op'] == 'play':
                function = data['params'][0]
                params = data['params'][1:]

                if function == 'nextmove':
                    self.game.lock.acquire()
                    success = self.game.nextmove(data['params'][0],data['params'][1])
                    board = self.game.getboard()
                    self.game.lock.release()
                    self.conn.send(dumps({'board': board,'success' : success}))

                elif function == 'save':
                    self.game.lock.acquire()
                    success = self.game.save(data['params'][0])
                    self.game.lock.release()
                    self.conn.send(dumps({'success': success}))

                elif function == 'load':
                    self.game.lock.acquire()
                    success = self.game.save(data['params'][0])
                    self.game.lock.release()
                    self.conn.send(dumps({'success': success}))



class CheckmateServer():

    def __init__(self):
        sock = socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0',20000))
        sock.listen(1)
        self.games = {}
        self.l = Lock()
        while True:
            conn, addr = sock.accept()
            agent = Agent(conn, addr, self)
            agent.start()

