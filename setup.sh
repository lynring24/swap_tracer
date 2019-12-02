#!/bin/bash 

echo "export path of swptracer"
SWPTRACE=$(pwd)/driver
echo "export SWPTRACE=${SWPTRACE}" >> ~/.bashrc
echo "export PYTHONPATH=\$PYTHONPATH:${SWPTRACE}" >> ~/.bashrc
source ~/.bashrc
