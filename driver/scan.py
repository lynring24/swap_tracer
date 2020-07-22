from utility import *

def scan_malloc():
    # check if file exist
    DRIVER=os.environ['SWPTRACE']
    if os.path.isfile(DRIVER+'/brew') == False:
       instr="cd %s; make ; cd %s;"%(DRIVER, get_path('root'))
       os.system(instr)

    clone_path = get_path('target')+'/clone'
    if os.path.isdir(clone_path):
        print "[DEBUG] Modified Target Exist"
    else:  
        ## TODO
        # create clone of the target
        print "$ create clone of target"
        os.system('sudo mkdir clone')
        os.system('for fname in `find "$(pwd)" -name "*.c"`; do $SWPTRACE/brew < $fname > ./clone${fname#$PWD}; done')
        os.system('sudo cp  -r `ls -A | egrep -v "\.$|[0-9]{4}-|clone|*.c"` clone')

        print "$ brew target"

        # os.system('cp %s/libhmalloc.a %s'%(DRIVER, clone_path))
        os.system('cp %s/hmalloc.* %s'%(DRIVER, clone_path))

        print "$ cd %s; make"%clone_path
        if os.system("cd  %s; make;"%clone_path) != 0: 
           print '[Fauilure] make in {}'.format(__file__)
           exit(1)

# os.system('for fname in `find \"$(pwd)\" -name \'*.c\'`; do echo ${fname:1} ; $SWPTRACE/brew < $fname > ./clone/${fname:2}; one')
# os.system('find "$(pwd)" -name \'*.c\' -exec sh -c \'$SWPTRACE/brew < $0 > ./clone${0#$PWD}\' {} \;')
#  find "$(pwd)" -name '*.c' -exec sh -c 'echo ${0#$PWD}' {} \;
 


