from threading import *
from socket import *
from json import *
import sys

from Checkmate import *


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
        global GAMEID
        self.id = GAMEID
        self.lock = Lock()
        self.cv = Condition(self.lock)
        GAMEID += 1
        self.activeplayers = 1
        self.active = True
        self.nextcolor = 'White'

        if params[0] == 'multi':
            self.capacity = 2
        else:
            self.capacity = 1


class Agent(Thread):
    def __init__(self, conn, addr, checkmateserver):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.checkmateserver = checkmateserver
        self.game = None
        self.color = None

    def run(self):
        rawdata = self.conn.recv(4096)
        if not rawdata:
            self.conn.shutdown(SHUT_RDWR)
            self.conn.close()
            return
        data = loads(rawdata.strip())

        if data['op'] == 'start':
            self.game = Game(data['params'])
            self.checkmateserver.l.acquire()
            self.checkmateserver.games[self.game.id] = self.game
            self.checkmateserver.l.release()
            if self.game.mode == 'multi':
                self.color = data['color']
            self.conn.send(dumps({'gameid': self.game.id}))

        elif data['op'] == 'connect':
            self.checkmateserver.l.acquire()
            game = self.checkmateserver.games[int(data['gameid'])]
            self.checkmateserver.l.release()
            if game.mode == 'multi':
                self.color = data['color']
            if game.capacity - game.activeplayers > 0:
                game.lock.acquire()
                game.activeplayers += 1
                game.lock.release()
                self.game = game
                self.conn.send(dumps({'success': True}))
                self.game.cv.acquire()
                self.game.cv.notifyAll()
                self.game.cv.release()
            else:
                self.conn.send(dumps({'success': False}))
                self.conn.shutdown(SHUT_RDWR)
                self.conn.close()
                return
        else:
            self.conn.send(dumps({'message': 'Wrong format'}))
            self.conn.shutdown(SHUT_RDWR)
            self.conn.close()
            return

        while True:
            print self.color,'1'
            if self.game.mode == 'multi':
                print self.color,'2'
                self.game.cv.acquire()
                print self.color,'3'
                if self.game.activeplayers < 2:
                    print self.color,'4'
                    while self.game.activeplayers < 2:
                        self.game.cv.wait()
                    print self.color,'5'
                else:
                    print self.color,'6'
                    while self.game.nextcolor != self.color:
                        self.game.cv.wait()
                    print self.color,'7'
                self.game.cv.release()
            print self.color,'8'

            if not self.game.active:
                self.game.lock.acquire()
                self.game.quit()
                self.game.lock.release()

                self.checkmateserver.l.acquire()
                del self.checkmateserver.games[self.game.id]
                self.checkmateserver.l.release()
                self.conn.send(dumps({'message': 'Game is killed'}))
                self.conn.shutdown(SHUT_RDWR)
                self.conn.close()
                self.game.cv.acquire()
                self.game.cv.notifyAll()
                self.game.cv.release()
                return

            rawdata = self.conn.recv(4096)
            if not rawdata:
                self.game.lock.acquire()
                self.game.activeplayers -= 1
                self.game.lock.release()
                self.conn.shutdown(SHUT_RDWR)
                self.conn.close()
                return
            data = loads(rawdata.strip())

            if data['op'] == 'exit':
                self.game.lock.acquire()
                self.game.activeplayers -= 1
                self.game.lock.release()
                self.conn.send(dumps({'message': 'You are detached'}))
                self.conn.shutdown(SHUT_RDWR)
                self.conn.close()
                return
            elif data['op'] == 'kill':
                self.game.lock.acquire()
                self.game.active = False
                if self.game.activeplayers == 1:
                    self.checkmateserver.l.acquire()
                    del self.checkmateserver.games[self.game.id]
                    self.checkmateserver.l.release()
                else:
                    self.game.activeplayers -= 1
                self.game.lock.release()
                self.conn.send(dumps({'success': True}))
                self.conn.shutdown(SHUT_RDWR)
                self.conn.close()
                return

            elif data['op'] == 'play':
                function = data['params'][0]
                params = data['params'][1:]

                if function == 'nextmove':
                    self.game.lock.acquire()
                    success = self.game.nextmove(params[0], params[1])
                    board = self.game.getboard()
                    isfinished = self.game.isfinished()
                    self.game.lock.release()
                    if success:
                        self.game.nextcolor = 'White' if self.game.nextcolor == 'Black' else 'Black'
                        self.game.cv.acquire()
                        self.game.cv.notifyAll()
                        self.game.cv.release()
                    if isfinished:
                        self.conn.send(dumps({'board': board, 'success': success, 'isfinished': isfinished}))
                    else:
                        self.conn.send(dumps({'board': board, 'success': success}))

                elif function == 'save':
                    self.game.lock.acquire()
                    success = self.game.save(params[0])
                    self.game.lock.release()
                    self.conn.send(dumps({'success': success}))

                elif function == 'load':
                    self.game.lock.acquire()
                    success = self.game.save(params[0])
                    self.game.lock.release()
                    self.conn.send(dumps({'success': success}))

                elif function == 'hint':
                    self.game.lock.acquire()
                    hint = self.game.hint()
                    self.game.lock.release()
                    self.conn.send(dumps({'hint': hint}))

                elif function == 'addbook':
                    self.game.lock.acquire()
                    success = self.game.addbook(params[0])
                    self.game.lock.release()
                    self.conn.send(dumps({'success': success}))

                elif function == 'enablebook':
                    self.game.lock.acquire()
                    success = self.game.enablebook(params[0])
                    self.game.lock.release()
                    self.conn.send(dumps({'success': success}))

                elif function == 'setbookmode':
                    self.game.lock.acquire()
                    success = self.game.setbookmode(params[0])
                    self.game.lock.release()
                    self.conn.send(dumps({'success': success}))

                elif function == 'getboard':
                    self.game.lock.acquire()
                    board = self.game.getboard()
                    self.game.lock.release()
                    self.conn.send(dumps({'board': board}))

                elif function == 'history':
                    self.game.lock.acquire()
                    history = self.game.history()
                    self.game.lock.release()
                    self.conn.send(dumps({'history': history}))

                elif function == 'quit':
                    self.game.lock.acquire()
                    self.game.active = False
                    if self.game.activeplayers == 1:
                        self.checkmateserver.l.acquire()
                        del self.checkmateserver.games[self.game.id]
                        self.checkmateserver.l.release()
                    else:
                        self.game.activeplayers -= 1
                    self.game.lock.release()
                    self.conn.send(dumps({'success': True}))
                    self.conn.shutdown(SHUT_RDWR)
                    self.conn.close()
                    self.game.cv.acquire()
                    self.game.cv.notifyAll()
                    self.game.cv.release()
                    return

                elif function == 'isfinished':
                    self.game.lock.acquire()
                    isfinished = self.game.isfinished()
                    self.game.lock.release()
                    self.conn.send(dumps({'isfinished': isfinished}))

                elif function == 'getwinner':
                    self.game.lock.acquire()
                    winner = self.game.getwinner()
                    self.game.lock.release()
                    self.conn.send(dumps({'winner': winner}))

                elif function == 'undo':
                    self.game.lock.acquire()
                    success = self.game.undo()
                    self.game.lock.release()
                    self.conn.send(dumps({'success': success}))

                elif function == 'setdepth':
                    self.game.lock.acquire()
                    self.game.setdepth(int(params[0]))
                    self.game.lock.release()

                elif function == 'getdepth':
                    self.game.lock.acquire()
                    depth = self.game.getdepth()
                    self.game.lock.release()
                    self.conn.send(dumps({'depth': depth}))

                elif function == 'getbookmode':
                    self.game.lock.acquire()
                    bookmode = self.game.getbookmode()
                    self.game.lock.release()
                    self.conn.send(dumps({'bookmode': bookmode}))

                elif function == 'newgame':
                    self.game.lock.acquire()
                    self.game.newgame()
                    board = self.game.getboard()
                    self.game.lock.release()
                    self.conn.send(dumps({'board': board}))

                elif function == 'changemode':
                    self.game.lock.acquire()
                    success = self.game.changemode(params[0])
                    self.game.lock.release()
                    self.conn.send(dumps({'success': success}))

                elif function == 'getmode':
                    self.game.lock.acquire()
                    mode = self.game.getmode()
                    self.game.lock.release()
                    self.conn.send(dumps({'mode': mode}))

                elif function == 'currentplayer':
                    self.game.lock.acquire()
                    currentplayer = self.game.currentplayer()
                    self.game.lock.release()
                    self.conn.send(dumps({'currentplayer': currentplayer}))


class CheckmateServer():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.games = {}
        self.l = Lock()
        self.sock = None

    def start(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        while True:
            conn, addr = self.sock.accept()
            agent = Agent(conn, addr, self)
            agent.start()


if __name__ == '__main__':
    checkmateserver = CheckmateServer(sys.argv[1], int(sys.argv[2]))
    checkmateserver.start()