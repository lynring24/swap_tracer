import os, sys

paths = []

if os.path.isdir(sys.argv[1]):
   for file in os.listdir('sys.argv[1]'):
       paths.append("%s/%s"%(sys.argv[1], file))
elif os.path.isfile(sys.argv[1]):
    paths.append(sys.argv[1])
else:
    print "invalide type"

os.system("mkdir -p mod")

os.system("flex brew.l")
# os.system("g++ lex.yy.c -lfl")
# g++ lex.yy.c -I/usr/lib/libfl.a
os.system('g++ -o brew lex.yy.c -I/usr/lib/libfl.a')
for file in paths :
    os.system("./brew < %s > mod/%s"%(file, file))

os.system("cp hmalloc.* mod")
os.system("gcc -o mod/main mod/main.c")
os.system("mod/main")


