#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -lt 1 ] && [ $# -gt 3 ]; then
	echo "Usage : $0 [-abstract] [mem limit in MiB] <command>"
	exit 1
fi 

exectime=$(LANG=en_us_88591; date +"%FT%T.%6N")

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
	sudo sh exec_mem_lim.sh $limit "$comm"
else
	eval $comm
fi

echo "trace down $comm"

SWAPTRACER_LOG="../demo/log"

mkdir -p $SWAPTRACER_LOG

if [ "$option" = true ]; then
sudo python trace.py -m "$exectime" "$comm" 
else
sudo python trace.py "$exectime" "$comm"
fi

generated_file=$(date -d "$exectime" +'%b%d%H%M%S')
python get_chopped_of.py  --noise-cancel ${SWAPTRACER_LOG}/${generated_file}.csv
