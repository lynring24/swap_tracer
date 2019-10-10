#!/bin/sh

CHECKTIMEFORMAT=$(cat /etc/rsyslog.conf | egrep ActionFileDefaultTemplate)

if [[ $CHECKTIMEFORMAT == *"#"* ]]; then 
   echo "rsyslog timestamping in RFC 3339 format"
else 
   echo "rsyslog timestamp traditional file format "
   cp /etc/rsyslog.conf /etc/rsyslog.conf.default
   cp ./rsyslog.conf.rfc3339 /etc/rsyslog.conf
fi
