#!
import os, sys, options, filelist, message,generator, select, time, signal
cread,swrite=os.pipe() #serv->client
sread,cwrite=os.pipe() #client -> serv
print(f"cread:{cread},swrite{swrite},sread:{sread},cwrite:{cwrite}",file=sys.stderr)
os.set_inheritable(cread,True)
os.set_inheritable(cwrite,True)
os.set_inheritable(sread,True)
os.set_inheritable(swrite,True)
to = float(options.args.timeout)
if options.args.DST=='.':
    options.args.DST==''

def numbers(c):
    if c =='0' or c=='1' or c=='2' or c=='3' or c=='4' or c=='5' or c=='6' or c=='7' or c=='8' or c=='9':
        return(int(c))
    else:
        return c

pid = os.fork()
if pid == 0:
    #code serveur
    oldpath=(os.getcwd())
    os.chdir(options.args.DST)
    l=filelist.list_only('.',options.args.recursive)
    l=generator.sort(l)
    filestocopy=[]
    if to == float(0):
        to = None
  
    (r,_,_)=select.select([sread],[],[],to)
    for read in r:
        msg = message.receive(sread)
        print("!!!!!!!!!!!!!!!!!!!!!! SERV READ !!!!!!!!!!!!!!!!!!!",file=sys.stderr)
        print(msg,file=sys.stderr)
        #reception filelist
        if type(msg)==list:
            if msg[0]=='filelist':
                msg.pop(0)
                pid2=os.fork()
                if pid2==0:
                    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!swrite :{swrite},pid2:{pid2}\n",file=sys.stderr)
                    #generator
                    a=(generator.compare(generator.sort(msg),l))
                    filestocopy+=a
                    (_,w1,_)=select.select([],[swrite],[],to)
                    for write in w1:
                        print("!!!!!!!!!!!!!!!!!!!!! IN SWRITE !!!!!!!!!!!!!!!!!!!!!",file=sys.stderr)
                        if filestocopy !=[]:
                            print("!!!!!!!!!!!!!!!!!!!!! SERV WRITE !!!!!!!!!!!!!!!!!!!!!",file=sys.stderr)
                            message.send(write,filestocopy)
                            os.close(write)
                    sys.exit(0)
                if pid2!=0:
                    os.waitpid(pid2,0)
                    #reception fichier
                    #time.sleep(5)
                    (r2,_,_)=select.select([sread],[],[],to)
                    for read in r2:
                        print("!!!!!!!!!!!!!!!!!!!!!! SERV READ2 !!!!!!!!!!!!!!!!!!!",file=sys.stderr)
                        msg=message.receive(read)
                        while msg!='end-of-files':
                            while msg=='start-of-file':
                                while msg !='end-of-file':
                                    msg=message.receive(read)
                                    print(f"!!!!!! MESSAGE SREAD2 {msg} !!!!!!!!!!!",file=sys.stderr)
                                    if type(msg) == str:
                                        print(msg)
                                        if msg=='end-of-file':
                                            break
                                        elif msg=='end-of-files':
                                            os.close(read)
                                            sys.exit(0)
                                    file=msg[1]
                                    path=msg[0]
                                    fd=os.open(path+file,os.O_CREAT | os.O_WRONLY)
                                    os.write(fd,msg[2])
                                msg=message.receive(read)
                            if msg[2]=='directory':
                                try:
                                    print(f"!!!!! MKDIR :{os.getcwd()+'/'+msg[0]+msg[1]}")
                                    os.mkdir(os.getcwd()+'/'+msg[0]+msg[1])
                                except:
                                    os.rmdir(os.getcwd()+'/'+msg[0]+msg[1])
                                    os.mkdir(os.getcwd()+'/'+msg[0]+msg[1])
                                msg=message.receive(read)
                        os.close(read)
    sys.exit(0)
else:
    #code sender
    filestocopyreceived=0
    if options.args.list_only :
        if options.args.recursive:
            filelist.list_only(options.args.DST, True)
        else:
            filelist.list_only(options.args.DST, False)
    if options.args.SRC != None:
        os.chdir(options.args.SRC)
    filestosend=[]
    l=[]
    l.append('filelist')
    l[1:]= filelist.list_only(os.getcwd(),options.args.recursive)
    if to == 0:
        to = None
    
    #envoi de la liste de fichiers
    (_,w3,_)=select.select([],[cwrite],[],to)          
    for write in w3:
        print("!!!!!!!!!!!!!!!!!!!!!! CLIENT WRITE !!!!!!!!!!!!!!!!!!!!",file=sys.stderr)
        value=l
        message.send(write,value)
    
    #reception filestocopy 
    (r4,_,_)=select.select([cread],[],_,to)
    for read in r4:
        print("!!!!!!!!!!!!!!!!!!!!!!!!! CLIENT READ !!!!!!!!!!!!!!!!!!!!",file=sys.stderr)
        a=message.receive(read)
        filestosend+=a
        print(f"!!!!!!!!!! FILESTOSEND RECEIVED: {filestosend}",file=sys.stderr)
        filestocopyreceived=1
        os.close(read)
    
    #envoi des fichiers
    if filestocopyreceived==1:
        (_,w5,_)=select.select([],[cwrite],[],to)
        for write in w5:
            print("!!!!!!!!!!!!!!!!!!!!! IN CWRITE2 !!!!!!!!!!!!!!!!!!!!!",file=sys.stderr)
            if filestosend != []:
                filestosend.append(('end-of-files','end-of-files'))
                print("!!!!!!!!!!!!!!!!!!!!! CLIENT WRITE2 !!!!!!!!!!!!!!!!!!!!!",file=sys.stderr)
                #tri afin de d'abord envoyer les directories à créer, dans l'ordre de leurs profondeurs
                dirlist=[]
                newfilestosend=[]
                for i,((path,files)) in enumerate(filestosend):
                    print((path,files))
                    path=path.split('/')[1:]
                    finalpath=''
                    for p in path:
                        if p!='':
                            finalpath+=p+'/'
                    file=files.split('//')[-1]
                    size=files.split('//')[0]
                    if type(numbers(size[0]))!=int:
                        if i != len(filestosend)-1:
                            dirlist.append((finalpath,file))
                    else:
                        newfilestosend.append(filestosend[i])
                filestosend=newfilestosend
                print(filestosend)
                print(dirlist)
                
                sorteddirlist=[]
                maxdepth=0
                for (finalpath,file) in dirlist:
                    path=finalpath.split('/')
                    if len(path)>maxdepth:
                        maxdepth=len(path)
                k=0
                while k<=maxdepth:
                    for i,(finalpath,file) in enumerate(dirlist):
                            if len(finalpath.split('/'))==k:
                                sorteddirlist.append((dirlist[i]))
                    k+=1
                print(f"!!!! SORTEDDIRLIST: {sorteddirlist}")
                sorteddirlist.pop(0)
                for (finalpath,dir) in sorteddirlist:
                    message.send(write,(finalpath,dir,'directory'))
                filestosend.append(('end-of-files','end-of-files'))
                print(f"!!!! FILESTOSEND: {filestosend}")
                #envoi des fichiers
                print(f"!!!!!!!!!! FILESTOSEND NODIR:{filestosend}")
                for i,(path,files) in enumerate(filestosend):
                    if path != 'end-of-files':
                        path=path.split('/')[1:]
                        finalpath=''
                        for p in path:
                            if p!='':
                                finalpath+=p+'/'
                        print(f"!!!!!!!!! FINALPATH: {finalpath}",file=sys.stderr)
                        file=files.split('//')[-1]
                        size=files.split('//')[0]
                        size=int(size)
                        message.send(write,'start-of-file')
                        while size >0:
                            fd=os.open(finalpath+file,os.O_RDONLY)
                            data=os.read(fd,4096)
                            print(data,file=sys.stderr)
                            size-=4096
                            message.send(write,(finalpath,file,data))
                        message.send(write,'end-of-file')
                    else:
                        message.send(write,path)
                        print(f"!!!!!!!!!! ALL FILES SENT GG !!!!!!!!!!!!!!!\n",file=sys.stderr)
                        os.close(write)
sys.exit(0)