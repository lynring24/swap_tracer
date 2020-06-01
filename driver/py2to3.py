import glob, os

for file in glob.glob('*.py'):
    if file != __file__: 
       os.system('py2to3 < %s > %s'%(file, file))
