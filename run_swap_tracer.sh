#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -lt 1 ] && [ $# -gt 3 ]; then
	echo "Usage : $0 [-m] [mem limit in MiB] <command>"
	exit 1
fi 

exectime=$(LANG=en_us_88591; date +"%Y %b %d %T")

if [ $# -eq 1 ]; then 
option=false
limit=-1
comm="$1"
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

if [ $limit -ne -1 ]; then 
	sudo sh lazybox/scripts/run_memcg_lim.sh $limit "$comm"
else
	eval $comm
fi

echo "trace down $comm"
#IFS=' ' read -ra path <<< $comm
#fname=${path[0]##*/}

mkdir -p plot
mkdir -p graph

if [ "$option" = true ]; then
sudo python trace.py -m "$exectime" "$comm" 
else
sudo python trace.py "$exectime" "$comm"
fi
