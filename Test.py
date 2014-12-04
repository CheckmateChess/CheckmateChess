from Checkmate import Checkmate
from socket import *

class Test:
    def send(self,s,command):
        s.send(command)
        print "----------------------------------------"
        print "Sent     :", command
        data = s.recv(4096)
        print "Received :", data
        print "----------------------------------------"
        return data