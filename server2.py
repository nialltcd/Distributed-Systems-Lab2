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
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
	print 'Creating Worker'
        Thread.__init__(self)
        self.tasks = tasks
	print 'Get Tasks'
        self.daemon = True
        self.start()
    
    def run(self):
	print 'RUN'
        while True:
            self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    print 'Server Created'

    # Create thread pool    
    pool = ThreadPool(5)
    print 'Thread Pool Created with 5 threads'

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
