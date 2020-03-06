from utility import *

TIME=0
TOP=1
BTM=2
FNAME=3
FUNC=4
VAR=5


def merge():
    print "$ create page table"
    with open(get_path('merge'), 'r') as merge:
         global page_table
         page_table = []
         for track in merge:
             item = [x.strip() for x in track.split(',')]
             if len(item) > 3 : 
                add_page_table(item)
             else:
                classify_area(item)
    merge.close()

def add_page_table(item):
    dump = [item[TIME], item[TOP], item[BTM], item[FNAME], item[FUNC], item[VAR]] 

    if dump in page_table:
        page_table.append(dump)
    else:
        page_table.append(dump)

def classify_area(item): 
       # run key and find the key that fits most
       output=open(get_path('total'), 'a+')
       page_table.sort(reverse=True)
       item[1]=item[1][:-2]
       print item
       if page_table is not None:
          for track in page_table:
              if track[TOP] <= item[TOP] and  item[TOP] <= track[BTM] and track[TIME] <= item[TIME]: 
                 # remove endline
                 print track
                 item.extend([track[FNAME], track[FUNC], track[VAR]])
                 print item
                 break
       
       line = ','.join(item) + "\n"
       output.write(line)


