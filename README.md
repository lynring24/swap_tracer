# Swap Tracer
![swaptracer](./icon.png)

Swap Tracer is an effective tool to visualize the change(swap) in memory and analyze it after executing the program. Currently, swap in/out and do_swap has been marked.

## Environment/Requirement
+ os : centos 7 ( linux series are available. )
+ kernel : 5.1.14 ( older versions are available also.)  
+ python : 2.7.5

## [Kernel Patch](https://github.com/lynring24/swap_tracer/blob/master/tracer_kernel.patch)
> patch -p0 < tracer_kernel.patch   

In kernel directory adapt patch file. It will add lines to mm/page_io.c and mm/memory.c.

## To Setup
Before using this swap tracer, configure the directory of log files from:

```
LOG_DIR_PATH="../log/" 
```
+ SWAPTRACER_PATH/driver/configure.py    
+ SWAPTRACER_PATH/driver/run.sh  


## How To Use
### run.sh
if you are using centos as OS try **sh** else try **bash
```$ sudo  [sh/bash]  SWAPTRACER_PATH/swaptracer/run.sh  \[--abstract\] \[--threshold\]  MEMLIMIT "COMMAND"        
ex) sudo  sh  run.sh  --threshold   256 "python cnn.py"
```

**sudo** Tracer reads log file which needs the permission of root. 

**--abstract**  for simpler version, output of the statistical mean value (optional)

**--threshold** track pages with over 10^THRESHOLD (optional)

**mem limit in MiB** limits the usage of memory (optional)

**command** programs to be run.


#### OUTPUT
run.sh will generate a **LOG_DIR_PATH/DATETIME\[_th\|_abs\].csv** and **LOG_DIR_PATH/DATETIME[_th]** which is a directory with split csv. 


## Directory 
+ kernel_patch
+ driver 
+ demo


### driver/trace.py
parse the input file and generate a **LOG_DIR_PATH/DATETIME.csv** containing lines of \[second, virtual page number\]

```
 $ python trace.py  \[--abstract\] \[--threshold\] \[src file path\]  "datetime(+%Y-%m-%dT%H:%M:%S.%6N")"  "COMMAND"   
ex) python trace.py   "2019-09-30T18:26:52.000000"   "./atmosphere_model"
```

### driver/split_by_block.py
splits the csv into block of data by the address and time

```
$ python   split_by_block.py   \[--threshold \]   FILENAME  
ex) python   split_by_block.py   --threshold  log/Sep30182652.csv
``` 

## OUTPUT : generated files 
Files are generated under the log directory based on **LOG_DIR_PATH** above. A main csv file is named after a start time  and partial csv are stored under a folder with a same of a main file.  

```
LOG
|_ Oct01234506.csv
|_ Oct01234506 
          |_ block_#.csv
          |_ block_#.csv
```
