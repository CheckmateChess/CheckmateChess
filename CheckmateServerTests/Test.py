from json import *


class Test:
    def send(self, s, command):
        s.send(command)
        print "----------------------------------------"
        print "Sent     :", command
        data = s.recv(4096)
        print "Received :", data
        asd = loads(data)

        if asd.get('board'):
            for row in asd['board']:
                print '             ',
                for frame in row:
                    print frame,
                print
        print "----------------------------------------"

        return data