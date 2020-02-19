test="/usr/share/swptracer/test.py"

print test

pos = test.rfind('/')+1

print test[:pos]+"mod/"+test[pos:]


