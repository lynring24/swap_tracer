#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -lt 2 ] || [ $# -gt 4 ]; then
	echo "Usage : $0 [--abstract] [--only-stackheap] <mem limit in MiB> <command>"
	exit 1
fi 

exectime=$(LANG=en_us_88591; date +"%FT%T.%6N")

ONLY_STACKHEAP=false
limit=${@: -2:1}
comm=${@: -1}
instruction="sudo python trace.py"

for var in "$@"
do
	case "$var" in
        --abstract)
	   instruction="${instruction} --abstract";;
	--only-stackheap)
	   ONLY_STACKHEAP=true
	   instruction="${instruction} --only-stackheap";;
        esac
done;

sudo sh exec_mem_lim.sh $limit "$comm"

SWAPTRACER_LOG="../demo/log"
mkdir -p $SWAPTRACER_LOG

instruction="${instruction} \"$exectime\" \"$comm\""
echo "$ ${instruction}"
eval "${instruction}"

output=$(date -d "$exectime" +'%b%d%H%M%S')

if $ONLY_STACKHEAP; then
instruction="python get_chopped_of.py ${SWAPTRACER_LOG}/${output}_osh.csv"
else
instruction="python get_chopped_of.py --only-stackheap ${SWAPTRACER_LOG}/${output}.csv"
fi

echo "$ ${instruction}"
eval "${instruction}"

