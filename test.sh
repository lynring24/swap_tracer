#!/bin/bash 
# Run a command and track the swap 

set -e 

if [ $# -lt 1 ] && [ $# -gt 3 ]; then
	echo "Usage : $0 [-m] [mem limit in MiB] <command>"
	exit 1
fi 


exectime1="2019 Aug 21 21:02:01"

exectime2="2019 Aug 21 21:20:01"

#sudo awk  'BEGIN { compare=date -d $exectime1 +"%Y %b %d %T"} /swptrace\(python\)/ {target=date -d $1FS$2FS$3 +"%b %d %T"; if (compare < target)
 #            if(NF==8){print $1FS$2FS$3FS$7FS$8} else {print$1FS$2FS$3FS$7FS$9} }' /var/log/messages > input_log1

#sudo awk  'BEGIN { compare=date -d "$exectime2" +"%Y %b %d %T"; print compare} /swptrace\(python\)/ {target=date -d $1FS$2FS$3 +"%b %d %T";if (compare < target)
#             if(NF==8){print $1FS$2FS$3FS$7FS$8} else {print$1FS$2FS$3FS$7FS$9} else {next} }' /var/log/messages > input_log2

sudo awk -v exectime="$exectime1" 'BEGIN { print exectimeFSyear;
	 year="date -r /var/log/messages +%Y"  } 
			/swptrace\(python\)/ {
		target=$yearFS$1FS$2FS$3;
		if (exectime < target)
			 {print "hello"} 
		else {print "next"} 
		}'  /var/log/messages  > output

