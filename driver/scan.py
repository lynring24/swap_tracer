from utility import *

def scan_malloc():
    # check if file exist
    try: 
	DRIVER=os.environ['SWPTRACE']
	if os.path.isfile(DRIVER+'/brew') == False:
	   print "$ flex brew " 
	   instr="cd %s; make ; cd %s;"%(DRIVER, get_path('root'))
	   os.system(instr)

	target = get_path('target')
	fpath = []
	dpath = [] 
	    

	if os.path.isfile(target):
	     fpath.append(target)
	       # add Makefile 
	     target = os.path.dirname(target)
	     fpath.append(target+"/Makefile")
        elif os.path.isdir(target):
             for root, directories, filenames in os.walk(target):
		 for directory in directories:
	 	     dpath.append(os.path.join(root, directory))
		 for filename in filenames:
	 	     fpath.append(os.path.join(root, filename))
	else:
	     print "[ERROR] invalid target"
	     exit(-1) 
	    
	moddir = get_path('root')+"/mod"
	print "mod dir :" +moddir
	if moddir[:-1] != '/':
	   moddir = moddir+"/"
	instr = "mkdir -p %s"%moddir
	os.system(instr)
	os.system('cp %s/hmalloc.* %s'%(DRIVER, moddir))
	    # check if sub directory exists
	for dir in dpath:
	    os.system("sudo mkdir -p %s"%dir)
	    
	for file in fpath :
	    fname = file.replace(target, moddir)
	    os.system("$SWPTRACE/brew < %s > %s"%(file, fname))
	    
	print "$ cd %s; make"%moddir
	if os.system("cd  %s; make;"%moddir) != 0: 
           raise Exception('[Fauilure] make in %s'%__file__)
    except:
       exit(1)

        


