#!/bin/bash 

exectime=$(LANG=en_us_88591; date +"%FT%T.%6N")

#sudo sh exec_mem_lim.sh 100 "python increment.py"


#cat /var/log/syslog |  awk -v date="${exectime}" -F, '/swptrace\(.*\)/ {if($1>date){print $1}}' > ${exectime}_log







