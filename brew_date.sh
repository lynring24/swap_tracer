#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -lt 1 ] && [ $# -gt 3 ]; then
	echo "Usage : $0 [-m] [mem limit in MiB] <command>"
	exit 1
fi 

exectime=$(date "+%Y %b %d %T")

sudo awk -v exectime="$exectime" '
/swptrace\(python\)/
{
target=$(date -d yearFS$1FS$2FS$3 "+%s");
 compare=$(exectime-target);
if (compare <= 0) {
          print$1FS$2FS$3FS$7FS$9}
 }
else 
{next}
}' /var/log/messages > mpas_log
 
