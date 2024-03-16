import os, stat, datetime, sys
from pathlib import Path

newl=[]
truc=0
def list_only(path,r):
    global newl
    global truc
    if truc==0:
        if path[-1] != '/':
            f = os.stat(path)
            dir=path.split('/')[len(path.split('/'))-1]
            mtime = datetime.datetime.fromtimestamp(f.st_mtime)
            size = str(f.st_size)
            mode = stat.filemode(f.st_mode)
            owner= Path(path).owner()
            newl.append('-directory'+'//'+size+'//'+mode+'//'+owner+'//'+mtime.strftime('%Y/%m/%d %H:%M:%S')+'//'+dir)
        truc = 1
    oldpath = os.getcwd()
    os.chdir(path)
    l = sorted(os.listdir(os.getcwd()))
    for files in l:
        f = os.stat(files)
        mtime = datetime.datetime.fromtimestamp(f.st_mtime)
        size = f.st_size
        mode = stat.filemode(f.st_mode)
        owner= Path(files).owner()
        if os.path.isfile(files):
            newl.append(str(size)+'//'+mode+'//'+owner+'//'+mtime.strftime('%Y/%m/%d %H:%M:%S')+'//'+files)
            #print(mode+' '+str(size)+' '+owner+' '+mtime.strftime('%Y/%m/%d %H:%M:%S')+' '+files,file=sys.stderr)
        elif (os.path.isdir(files) | os.path.islink(files)):
            if r:
                newl.append('-directory-'+'//'+mode+'//'+owner+'//'+mtime.strftime('%Y/%m/%d %H:%M:%S')+'//'+files)
               # print(mode+' '+str(size)+' '+owner+' '+mtime.strftime('%Y/%m/%d %H:%M:%S')+' '+files+' Directory :',file=sys.stderr)
                list_only(files,r)
            else:
                newl.append('-directory-'+'//'+mode+'//'+owner+'//'+mtime.strftime('%Y/%m/%d %H:%M:%S')+'//'+files)
                #print(mode+' '+str(size)+' '+owner+' '+mtime.strftime('%Y/%m/%d %H:%M:%S')+' '+files,file=sys.stderr)
    newl.append('-end-of-directory-')
    os.chdir(oldpath)
    return newl

if __name__ == '__main__':
    print("Hello, world !")
    path = '../'
    r = True
    newl = list_only(path,r)
    print(newl)