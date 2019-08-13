#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -ne 2 ] && [ $# -ne 3 ]; then
	echo "Usage : $0 [-m] <mem limit in MiB> <command>"
	exit 1
fi 

exectime=$(date "+%b %d %H:%M:%S")

if [ $1 = "-m" ]; then 
option=true
limit=$2
comm="$3"
else
option=false
limit=$1
comm="$2"
fi


sudo sh lazybox/scripts/run_memcg_lim.sh $limit "$comm"
echo "trace down $comm"
IFS=' ' read -ra path <<< $comm
fname=${path[0]##*/}

mkdir -p swaptracer/plot
mkdir -p swaptracer/log

if [ "$option" = true ]; then
sudo python trace.py -m "$exectime" "$comm" 
else
sudo python trace.py "$exectime" "$comm"
fi
