#!/bin/bash

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

echo ${CURRENT_LOG}
mkdir -p ${SWAPTRACER_LOG}
mkdir -p ${CURRENT_LOG}
