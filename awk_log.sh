#!/bin/bash

# awk -F, '{gsub(/[-:]/," ",$2);gsub(/[-:]/," ",$3);d2=mktime($3);d1=mktime($2);print $1","d2-d1,"secs";}' /var/log/messages > awk_log
# awk  '{ TIME=2019FS$1FS$2FS$3; print TIME;}' /var/log/messages 
awk  '{  month="01"; switch($1) {
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
print month;
TIME=2019" "month" "$2" "$3; gsub(/:/," ",TIME); print TIME mktime(TIME);}' /var/log/messages 
