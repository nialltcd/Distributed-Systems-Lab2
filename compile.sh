#!/bin/bash

#./server.py
count=0
while [ $count -lt 100 ]
do
./client.py 8000 $count
count=$[$count+1]
done
./client.py 8000 'KILL_SERVICE'
