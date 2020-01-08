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
```
sh setup.sh
source ~/.bashrc
```
### run  

```
$ python $SWPTRACE/exec.py <--mem=Mib> <--cmd="command to run"> <--ip=public ip> <--port=port number> 

# <options> are for quick setup.
```
[optional] 
Before using this swap tracer, modify **driver/configure.json** if needed.
This will be a default setting.
```
{
        "MEM_LIMIT": memory limit in MiB,
	"COMMAND": command to run,
	"PATH": {
		"LOG_ROOT": path for log directory, MUST BE ABSOLUTE PATH 
	},
        "ABSTRACT": option to abstract data using spatial locality (default true),
        "THRESHOLD": user-defined threshold for vma (default -1 if not used) 
}
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

![plot](./demo/plot/increment.png)


## Directory 
+ swptracer.patch
+ driver 
+ driver/templates
+ driver/unittest (for checkup)
+ demo/log
+ demo/code
+ demo/plot

