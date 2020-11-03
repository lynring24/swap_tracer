# swptracer
![ swptracer](./icon.png)

 **swptracer** is an effective tool to visualize the change(swap) in memory and analyze it after executing the program. Memory movement (swap in, out) could be tracked and summarized by swptracer.   

## Environment/Requirement
+ os : centos 7 ( linux series are available. )
+ kernel : 5.1.14 ( older versions are available also.)  
+ python : 2.7.5
+ plotly : for visualization

## [Kernel Patch](https://github.com/lynring24/swptracer/blob/master/tracer_kernel.patch)
> patch -p0 < $SWPTRACE/../swptracer.patch   

In kernel directory adapt patch file. It will add lines to mm/page_io.c and mm/memory.c.

## How To Use
### Setup
1. Disable **/etc/rsyslog.conf** option
```
# Use traditional timestamp format.
# To enable high percision timestamps, comment out the following line
#
# $ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat <- Here
```
2. Run script and compile  
```
# run setup
$ cd /PATH_TO_SWPTRACER_ROOT/
$ sh setup

# to check setup
$ echo $SWPTRACE
$ source ~/.bashrc

$ cd driver
$ make 

# install requisite package
# python=2.7.*
$ pip install $(cat requisite)
$ apt-get install python-tk
```
3. [Optional] Adding the linkage for profiling
For the profiling, please include the linkage(**-L. -lhmalloc**) to the Makefile of your target source 
For example, 
```
martix_multiplication:
	gcc matrix.c -lm -o matrix_multiplication
```
should be
```
matrix_multiplication:
	# gcc matrix.c -lm -L. -lhmalloc -o matrix_multiplication
	# gcc -o matrix malloc.c -g -lm -Wl,--no-as-needed -ldl
```

### Execution

```
$ python $SWPTRACE/exec.py <--mem=Mib> <--cmd="command to run"> \
	<--ip=public ip> <--port=port number> <--log="/Absolute_path_for_log_dir/"> 

# <> is optional

```

### OUTPUT
```
LOG_ROOT
|
| YYYY-MM-DDTHH:MM:SS.msec
          |  LOG_FILES.csv
```
### plot

![plot](./example.gif)

## Directory 
+ swptracer.patch
+ driver 
+ driver/templates
+ demo
