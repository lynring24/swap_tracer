import os,sys

flist = os.listdir('.')

for fname in flist:
    if 'py' in fname  and fname != 'read.py':
        print fname
        with open(fname, 'r') as src: 
            for line in src: 
                if 'open(get_path(' in line:
                    print fname, line

