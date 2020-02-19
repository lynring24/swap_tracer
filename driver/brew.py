from common import *

def scan_to_hook():
    paths = []
    targetdir = get_path('target')
    if os.path.isdir(targetdir):
       for file in os.listdir(targetdir):
           paths.append("%s/%s"%(targetdir, file))
    elif os.path.isfile(targetdir):
         paths.append(targetdir)
    else:
        print "invalide type"

    os.system("mkdir -p %s/mod"%get_path('root'))
    os.system("flex brew.l")
    os.system('g++ -o brew lex.yy.c -I/usr/lib/libfl.a')
    for file in paths :
        pos = file.rfind('/')+1
        modpath = file[:pos]+"mod/"+file[pos:]
        os.system("./brew < %s > %s"%(file, modpath ))
    os.system("cd mod; make")


