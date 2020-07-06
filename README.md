# swptracer
![ swptracer](./icon.png)

 **swptracer** is an effective tool to visualize the change(swap) in memory and analyze it after executing the program. Currently, swap in/out and do_swap has been marked.

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
$ cd /PATH_TO_SWPTRACER_DIR/
$ sh setup

# to check setup
$ echo $SWPTRACE
$ source ~/.bashrc

$ cd driver
$ make 
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
	gcc matrix.c -lm -L. -lhmalloc -o matrix_multiplication
```

#### PATH SETTING 
Before using this swap tracer, modify **driver/configure.json** if needed.
This will be a default setting.

```
{
        "MEM_LIMIT"  : memory limit in MiB,
	"COMMAND"    : command to run,
        "PUBLIC"  : {
              "IP"   : public ip you need,
              "PORT" : port number,
        },
	"PATH": {
		"LOG_ROOT": path for log directory, MUST BE ABSOLUTE PATH 
	}
}
```
### run  

```
$ python $SWPTRACE/exec.py <--mem=Mib> <--cmd="command to run"> <--ip=public ip> <--port=port number> 

# <options> are for quick setup.
```

### OUTPUT
```
LOG_ROOT
|
| YYYY-MM-DDTHH:MM:SS.msec
          |  awk.log  
          |  extracted.log
```
### plot

![plot](./example.gif)


## Directory 
+ swptracer.patch
+ driver 
+ driver/templates
+ driver/unittest (for checkup)
+ demo

