#!/bin/bash

exectime="Sep 1 16:00:00"
start="2019 08 20 16:00:00"
#start=$(date "+%Y %m %d %H:%M:%S") 


awk -v start="$start" 'BEGIN{ gsub(/:/, " ", start); print start, mktime(start); }{  month="01"; switch($1) {
 case  "Feb" : month="02"; break;
 case  "Mar" : month="03"; break;
 case  "Apr" : month="04"; break;
 case  "May" : month="05"; break;
 case  "Jun" : month="06"; break;
 case  "Jul" : month="07"; break;
 case  "Aug" : month="08"; break;
 case  "Sep" : month="09"; break;
 case  "Oct" : month="10"; break;
 case  "Nov" : month="11"; break;
 case  "Dec" : month="12"; break;
 default:  break;
 }
TIME=2019" "month" "$2" "$3; gsub(/:/," ",TIME); 
  if (mktime(start) < mktime(TIME) ) 
    print "start <  time by " mktime(start) " to " mktime(TIME);
   else 
    print "start > time by "  mktime(start) " to " mktime(TIME);}' /var/log/messages 
