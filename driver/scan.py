from utility import *

def scan_malloc():
    # check if file exist
    try: 
	DRIVER=os.environ['SWPTRACE']
	if os.path.isfile(DRIVER+'/brew') == False:
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
	    
	mod_path = get_path('root')
        if mod_path[-1] != '/':
            mod_path = mod_path+"/mod"
        
        if os.path.isdir(mod_path):
            print "[DEBUG] Modified Target Exist"
        else: 
            print "$ mkdir {}".format(mod_path)
            instr = "mkdir -p %s"%mod_path
            os.system(instr)

            print "$ copy target"
            
            # check if sub directory exists
            for dir in dpath:
                os.system("sudo mkdir -p %s"%dir)
                
            print "$ brew target"
            for file in fpath :
                if "*.h" not in file:
                    fname = file.replace(target, mod_path)
                    if ".c" in fname:
                        os.system("$SWPTRACE/brew < %s > %s"%(file, fname))
                    else:
                        os.system("cp {} {}".format(file, fname))

            # os.system('cp %s/libhmalloc.a %s'%(DRIVER, mod_path))
            os.system('cp %s/hmalloc.* %s'%(DRIVER, mod_path))

            print "$ cd %s; make"%mod_path
            if os.system("cd  %s; make;"%mod_path) != 0: 
               raise Exception('[Fauilure] make in %s'%__file__)
    except:
       exit(1)

        


