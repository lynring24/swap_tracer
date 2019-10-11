#!/bin/bash

sudo bash run_swap_tracer.sh 256 "python ../demo/code/cnn.py" &

sleep 300
PID=$(ps -ef | grep python | awk '{print $2}')
echo "pid : $PID"

count=0
while [ -n "$#1" -a -e  /proc/$PID ] 
do
	count=$(($count+1))
	cat /proc/$PID/smaps > smaps$count
	sleep 120 # interval 2min
done


