#!/bin/bash

rm main
rm hook.so 
set -e 


gcc -o hook.so hook.c -g -fPIC -shared -Wl,--no-as-needed -ldl 
gcc -o main -g main.c 

#LD_PRELOAD=./hook.so 
#export LD_PRELOAD=./hook.so

echo "execute main"
#./main
