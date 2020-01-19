#!/bin/bash

vi hook.cpp
g++ -fPIC -shared -o hook.so hook.cpp -ldl
vi main.cpp
gcc -o main main.cpp
vi main.cpp
g++ -o main main.cpp
./hook ./main
LD_PRELOAD=./hook.so ./main 
