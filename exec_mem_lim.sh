#!/bin/bash
#
# Run a command with memory cgroup that has specific memory limit

if [ $# -ne 2 ]
then
	echo "Usage: $0 <mem limit in MiB> <command>"
	exit 1
fi

MEMLIM=$(($1 * 1024 * 1024))
COMM=$2

MEMCG_ORIG_DIR=/sys/fs/cgroup/memory/
MEMCG_DIR=/sys/fs/cgroup/memory/run_mem_lim_$USER
sudo mkdir $MEMCG_DIR

sudo bash -c "echo $$ >> $MEMCG_DIR/cgroup.procs"
sudo bash -c "echo $MEMLIM > $MEMCG_DIR/memory.limit_in_bytes"

rm -rf history.2014-09-10_00.00.00.nc
rm -rf diag.2014-09-10_00.00.00.nc

echo "COMM: $COMM"

eval "$COMM"

#sudo rmdir $MEMCG_DIR
