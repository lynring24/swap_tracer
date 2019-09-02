#!/bin/bash 
# Run a command and track the swap 

set -e 

exectime=$(date "+%Y %b %d %T")
year=$(date -r /var/log/messages "+%Y")

sudo awk -v exectime="$exectime" -v year="$year" 'BEGIN {
 print exectime FS year }
{
 target=$yearFS$1FS$2FS$3;
 if (exectime >= target) {
       next
 } 
}' /var/log/messages 
 
