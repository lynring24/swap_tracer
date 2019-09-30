# Swap Tracer
![swaptracer](./icon.png)

Swap Tracer is an effective tool to visualize the change(swap) in memory and analyze it after executing the program. Currently, swap in/out and do_swap has been marked.

## Environment/Requirement
+ os : centos 7 ( linux series are available. )
+ kernel : 5.1.14 ( older versions are available also.)  
+ python : 2.7.5
+ [lazybox](https://github.com/sjp38/lazybox) : work of @sjp38, if needed for the limited memory usage(optional).
+ [gnuplot](http://www.gnuplot.info/) : a visualization tool (optional).

## [Kernel Patch](https://github.com/lynring24/swap_tracer/blob/master/tracer_kernel.patch)
> patch -p0 < tracer_kernel.patch   

In kernel directory adapt patch file. It will add lines to mm/page_io.c and mm/memory.c.

## To Setup
Before using this swap tracer, configure the directory of log files from:

```
LOG_DIR_PATH="../log/" 
```
+ SWAPTRACER_PATH/driver/configure.py   # line no : 6 
+ SWAPTRACER_PATH/driver/run\_swap\_tracer.sh  # line no : 40


## How To Use
### run_swap_tracer.sh
Since there might be a data locality, trace could be done in more abstracted mode with option [-m].

> $ sudo  sh   SWAPTRACER_PATH/swaptracer/run_swap_tracer.sh  \[--abstract\] \[--only-stackheap\]  MEMLIMIT "COMMAND"        
ex) sudo  sh run_swap_tracer.sh "python cnn.py"  
ex) sudo  sh  run_swap_tracer.sh   524   "python cnn.py"  
ex) sudo  sh  run_swap_tracer.sh  --abstract   256 "python cnn.py"
ex) sudo  sh  run_swap_tracer.sh  --only-stackheap   256 "python cnn.py"

<pre>
**sudo**  Tracer reads log file which needs the permission of root.
**--abstract** option for simpler version, output of the statistical mean value(optional).
**--only-stackheap** track memory only around stack and heap
**mem limit in MiB** limits the usage of memory. (optional)
**command** programs to be run.
</pre>

#### Result
run_swap_tracer.sh will generate a **LOG_DIR_PATH/DATETIME\[_osh\|_abs\].csv** and **LOG_DIR_PATH/DATETIME[_osh]** which is a directory with split csv. 


## Directory 
+ kernel_patch
+ driver 
+ demo


### driver/trace.py
parse the input file and generate a LOG_DIR_PATH/DATETIME.csv containing lines of \[microsecond, virtual memory address\]

> $ python trace.py  \[--abstract\] \[--only-stackheap\] \[src file path\]  "datetime(+%Y-%m-%dT%H:%M:%S.%6N")"  "COMMAND"   
ex) python trace.py   "2019-09-30T18:26:52.000000"   "./atmosphere_model"

### driver/get_chopped.py
splits the csv into block of data by the address and time

> $ python     get_chopped.py     \[--only-stackheap \]   FILENAME             
ex) python     get_chopped_of.py     --only-stackheap   log/Sep30182652.csv
 
<pre>
 generated folder = LOG_DIR_PATH/DATETIME or LOG_DIR_PATH/DATETIME_osh
 noise-cancel option ignores swap near virtual memory address 0 (가상 메모리의 entry 0번 때 페이지들을 제외하고 데이터를 추출함) 
 without --noise-cancel generates LOG_DIR_PATH/DATETIME 
</pre>
