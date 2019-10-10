#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -lt 2 ] || [ $# -gt 4 ]; then
	echo "Usage : $0 [--abstract] [--threshold] <mem limit in MiB> <command>"
	exit 1
fi 

sh setup.sh

exectime=$(LANG=en_us_88591; date +"%FT%T.%6N")

ONLY_STACKHEAP=false
limit=${@: -2:1}
comm=${@: -1}
instruction="sudo python trace.py"

SWAPTRACER_LOG="../demo/log"
mkdir -p $SWAPTRACER_LOG

sudo sh exec_mem_lim.sh $limit "$comm"

# run command and get the pid 
#sudo sh exec_mem_lim.sh $limit "$comm" & PID=$(ps | grep python | awk '{print $1}')
#cat /proc/${PID}/smaps > smaps

for var in "$@"
do
	case "$var" in
        --abstract)
	   instruction="${instruction} --abstract";;
	--threshold)
	   ONLY_STACKHEAP=true
	   instruction="${instruction} --threshold";;
        esac
done;

instruction="${instruction} \"$exectime\" \"$comm\""
echo "$ ${instruction}"
eval "${instruction}"

output=$(date -d "$exectime" +'%b%d%H%M%S')

if $ONLY_STACKHEAP; then
instruction="python split_by_block.py ${SWAPTRACER_LOG}/${output}_th.csv"
else
instruction="python split_by_block.py --threshold ${SWAPTRACER_LOG}/${output}.csv"
fi

echo "$ ${instruction}"
eval "${instruction}"

