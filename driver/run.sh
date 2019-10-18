#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -lt 2 ] || [ $# -gt 4 ]; then
echo "Usage : $0 [--abstract] [--threshold] <mem limit in MiB> <command>"
exit 1
fi 

#bash configure.sh
CHECKTIMEFORMAT=$(cat /etc/rsyslog.conf | egrep ActionFileDefaultTemplate)
if [[ $CHECKTIMEFORMAT == *"#"* ]]; then
        echo "rsyslog timestamping in RFC 3339 format"
else  
	echo "rsyslog timestamp traditional file format "
	cp /etc/rsyslog.conf /etc/rsyslog.conf.default
        cp ./rsyslog.conf.rfc3339 /etc/rsyslog.conf
fi


SWAPTRACER_LOG="../demo/log"
exectime=$(LANG=en_us_88591; date +"%FT%T.%6N")
CURRENT_LOG=${SWAPTRACER_LOG}/${exectime}
export exectime
export CURRENT_LOG

mkdir -p ${SWAPTRACER_LOG}
mkdir -p ${CURRENT_LOG}


# get passed parameter 
ONLY_STACKHEAP=false
limit=${@: -2:1}
comm=${@: -1}


sudo sh exec_mem_lim.sh $limit "$comm"

# run command and get the pid 
#sudo sh exec_mem_lim.sh $limit "$comm" & PID=$(ps | grep python | awk '{print $1}')
#cat /proc/${PID}/smaps > smaps


#cat /var/log/syslog |  awk -v date="${exectime}" -F, '/swptrace\(.*\)/ {if($1>date){print $1}}' > ${CURRENT_LOG}/log


echo "${CURRENT_LOG}"


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

instruction="${instruction} ${CURRENT_LOG}/log  \"${exectime}\" \"$comm\""
echo "$ ${instruction}"
eval "${instruction}"


#output=$(date -d "$exectime" +'%b%d%H%M%S')
if $ONLY_STACKHEAP; then
instruction="python split_by_block.py ${CURRENT_LOG}/extracted_th.csv"
else
instruction="python split_by_block.py --threshold ${CURRENT_LOG}/extracted.csv"
fi

echo "$ ${instruction}"
eval "${instruction}"

unset exectime
unset CURRENT_LOG
