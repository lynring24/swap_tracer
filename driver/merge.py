from utility import *

TIME=0
TOP=1
BTM=2
FNAME=3
FUNC=4
VAR=5

ALLOC='0'
SWP='1'

def merge():
    print "$ record page info"
    with open(get_path('merge'), 'r') as merge:
         global page_table
         page_table = []
         for track in merge:
             item = [x.strip() for x in track.split(',')]
             if len(item) > 2 : 
                add_page_table(item)
             else:
                classify_area(item)
    merge.close()
    if is_false_generated(get_path('total')):    
        print "Swap did not occure"
        clean_up_and_exit(get_path('total'), 'merge')

def write(line): 
    output=open(get_path('total'), 'a+')
    output.write(line)



def add_page_table(item):
    dump = [item[TIME], item[TOP], item[BTM], item[FNAME], item[FUNC], item[VAR]] 
    page_table.append(dump)
    item=dump[:2]+dump[3:]+[ALLOC]
    line = ','.join(item) + "\n"
    write(line)


def classify_area(item): 
       # run key and find the key that fits most
       page_table.sort(reverse=True)
       item[1]=item[1][:-2]
       if page_table is not None:
          for track in page_table:
              if track[TOP] <= item[TOP] and item[TOP] <= track[BTM] and track[TIME] <= item[TIME]: 
                 # remove endline
                 item.extend([track[FNAME], track[FUNC], track[VAR]])
                 break       
       item.append(SWP)
       line = ','.join(item) + "\n"
       write(line)
