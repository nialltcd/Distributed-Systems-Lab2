#!/usr/bin/python

import SocketServer
from Queue import Queue
from threading import Thread

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
	print 'New Connection'
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
	if 'KILL_SERVICE' in self.data:
		print 'KILL'
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    print 'Server Created'

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
