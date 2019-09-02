#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -lt 1 ] && [ $# -gt 2 ]; then
	echo "Usage : $0 [-m] [mem limit in MiB] \"./atmosphere_model\""
	exit 1
fi 

if [ $# -eq 1 ]; then 
option=false
limit=-1
comm="./atmosphere_model"
else 
	if [ $1 = "-m" ]; then 
		option=true
		limit=$2
		comm="$3"
	else
		option=false
		limit=$1
		comm="$2"
	fi
fi

# there are memory limitation needed use lazybox
# else run command 


journal_time=$(date "+%Y-%m-%d %T")
log_time=$(date "+%Y %b %d %T")

if [ $limit -ne -1 ]; then 
	sudo sh exec_mem_lim.sh $limit "$comm"
else
	eval $comm
fi

echo "trace down $comm"

mkdir -p plot
mkdir -p graph

journalctl --since="$journal_time" > mpas_log

if [ "$option" = true ]; then
sudo python trace.py -m  mpas_log "$log_time" "$comm" 
else
sudo python trace.py mpas_log "$log_time" "$comm"
fi

rm -f mpas_log
