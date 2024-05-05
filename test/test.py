import os
import marshal
import py_compile
import os
import imp

def generate(code):
    codeobject = compile(code, '', 'exec')
    with open('test.pyc', 'wb') as f: 
        f.write('\0\0\0\0')
        timestamp = int(os.fstat(f.fileno()).st_mtime)
        py_compile.wr_long(f, timestamp)
        marshal.dump(codeobject, f) 
        f.flush()
        f.seek(0, 0)
        MAGIC = imp.get_magic()
        f.write(MAGIC)

folders = os.listdir('.')
for folder in folders:
    if folder[1] != '.': continue
    file = folder[2:]
    print file
    f = open("./"+folder+'/'+file+'.py')
    code = f.read()
    f.close()
    os.system('echo "\n'+file+':" >> result1')
    os.system('echo "\n'+file+':" >> result2')
    generate(code)
    os.system('python2 test.pyc >> result1')
    os.system('mv test.pyc ../test.pyc')
    os.system('cd ..;./pythonvm test.pyc >> test/result2')
    