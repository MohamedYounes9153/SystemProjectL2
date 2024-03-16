import os, sys

def sort(list):
    src='../'
    newlist=[]
    pile=src.split('/')[:len(src.split('/'))-1]
    
    pile[0]+='/'
    for files in list:
        f=files.split('//')
        if f[0]=='-directory-':
            path=src
            for p in pile:
                if not p == src:
                    path+= p+'/'
            newlist.append((path,files))
            pile.append(f[-1])
        elif f[0]=='-end-of-directory-':
            pile.pop()
        else:
            path=src
            for p in pile:
                if not p == src:
                    path+= p+'/'
            newlist.append((path,files))
    return(newlist)

def compare(lcopy,lpaste):
    filestocopy=[]
    filestodelete=[]
    for file in (lcopy):
        if file not in lpaste:
            filestocopy.append(file)
    return(filestocopy)

def delete(lcopy,lpaste):
    filestodelete=[]
    for files in lpaste:
        if files not in lcopy:
            filestodelete.append(files)
    return (filestodelete)