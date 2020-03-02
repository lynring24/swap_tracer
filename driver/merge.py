from utility import *

TIME=0
FNAME=1
LINE=2
FUNC=3
VAR=4
TOP=5
BTM=6
VMA=1


def merge():
    print "$ create page table"
    with open(get_path('merge'), 'r') as merge:
         global page_table
         page_table = []
         for track in merge:
             item = track.split(',')
             if len(item) > 2 : 
                add_page_table(item)
             else:
                classify_area(item)
    merge.close()

def add_page_table(item):
    dump = [item[TIME], item[FNAME], item[LINE], item[FUNC], item[VAR], item[TOP], item[BTM]] 

    if dump in page_table:
        page_table.append(dump)
    else:
        page_table.append(dump)

def classify_area(item): 
       # run key and find the key that fits most
       output=open(get_path('total'), 'a+')
       page_table.sort(reverse=True)
       print page_table[0][0], page_table[-1][0]
       item[1]=item[1][:-2]
       for track in page_table:
           if track[TOP] <= item[VMA] and  item[VMA] <= track[BTM] and track[TIME] <= item[TIME]: 
              # remove endline
              item.extend({track[FNAME], track[LINE], track[FUNC], track[VAR]})
              break
       
       line = ','.join(item) + "\n"
       output.write(line)


