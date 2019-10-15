#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -lt 2 ] || [ $# -gt 4 ]; then
	echo "Usage : $0 [--abstract] [--threshold] <mem limit in MiB> <command>"
	exit 1
fi 

bash setup.sh

exectime=$(LANG=en_us_88591; date +"%FT%T.%6N")

ONLY_STACKHEAP=false
limit=${@: -2:1}
comm=${@: -1}


SWAPTRACER_LOG="../demo/log"
CURRENT_LOG=${SWAPTRACER_LOG}/${exectime}
mkdir -p $SWAPTRACER_LOG

sudo sh exec_mem_lim.sh $limit "$comm"

# run command and get the pid 
#sudo sh exec_mem_lim.sh $limit "$comm" & PID=$(ps | grep python | awk '{print $1}')
#cat /proc/${PID}/smaps > smaps

mkdir -p ${CURRENT_LOG}

cat /var/log/syslog |  awk -v date="${exectime}" -F, '/swptrace\(.*\)/ {if($1>date){print $1}}' > ${CURRENT_LOG}/log

instruction="sudo python trace.py "

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

instruction="${instruction}  ${CURRENT_LOG}/log  \"$exectime\" \"$comm\""
echo "$ ${instruction}"
eval "${instruction}"

output=$(date -d "$exectime" +'%b%d%H%M%S')

if $ONLY_STACKHEAP; then
instruction="python split_by_block.py ${CURRENT_LOG}/parse_log_th.csv"
else
instruction="python split_by_block.py --threshold ${CURRENT_LOG}/parse_log.csv"
fi

echo "$ ${instruction}"
eval "${instruction}"

