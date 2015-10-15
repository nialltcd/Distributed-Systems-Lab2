#!/usr/bin/python

import socket
import sys
from threading import *
from Queue import Queue
import re
import os

global port
global host

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            client_connection = self.tasks.get()
            try: self.process_message(client_connection)
            except Exception, e: print e
            self.tasks.task_done()
	
    def process_message(self,client_connection):
	data=client_connection.recv(1024)#[2:-2]
	print data
	global port,host
	if re.match('^HELO\s.*', data):
		text = data[5:]
		client_connection.send('HELO '+text+'\nIP:['+host+']\nPort:['+str(port)+']\nStudentID:[b7b3def745dde423b09fdbbd94f1f46405c629639a4c0480b04070d46c1774e6]\n')
	elif re.match('^KILL_SERVICE$',data):
	        client_connection.send('Killing Service!\nIP:['+host+']\nPort:['+str(port)+']\nStudentID:[b7b3def745dde423b09fdbbd94f1f46405c629639a4c0480b04070d46c1774e6]\n')
		os._exit(0)
	else:
		client_connection.send('Incorrect string format received: '+data+'\nIP:[ip address]\nPort:[port number]\nStudentID:[b7b3def745dde423b09fdbbd94f1f46405c629639a4c0480b04070d46c1774e6]\n')


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self,client_connection ):
        """Add a task to the queue"""
        self.tasks.put(client_connection)

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
global host
host="127.0.0.1"
global port
port = int(sys.argv[1])
serversocket.bind((host, port))
pool = ThreadPool(5)
serversocket.listen(10)
while 1:
    clientsocket, address = serversocket.accept()
    pool.add_task(clientsocket)
