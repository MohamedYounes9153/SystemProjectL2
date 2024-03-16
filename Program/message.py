import os,sys, pickle,select,time

def send(fd,v,tag=None):
    print(f"!!!SENDING {v} to :{fd}\n",file=sys.stderr)
    v=memoryview(pickle.dumps(v))
    size=len(v)
    
   
    #envoi du message
    os.write(fd,size.to_bytes(4,'big'))
    while v:
        sent = os.write(fd,v)
        print(f"!!!SENT:{v} to:{fd}\n",file=sys.stderr)
        v = v[sent:]
        
def receive(fd):
    print(f"!!!RECEIVING from :{fd}\n",file=sys.stderr)
    buffersize = 16384
    size = os.read(fd, 4)
    if not size:
        print(f"!!!NO DATA RECEIVED from :{fd}\n",file=sys.stderr)
        return 'Message vide'
    size = int.from_bytes(size, 'big')
    print(f"!!!SIZE:{size}\n",file=sys.stderr)
    msg = b''
    while len(msg)<size:
        rsize = min(buffersize,size-len(msg))
        r, w, e = select.select([fd], [], [], 0)
        if not r:
            time.sleep(0.1)
            continue
        buffer = os.read(fd, rsize)
        if not buffer:
            break
        print(f"buffer:{buffer}\n", file=sys.stderr)
        msg += buffer
    try:
        msg = pickle.loads(msg)
    except:
        msg = 'Message vide'
    print(f"!!!FINAL msg received :{msg}\n", file=sys.stderr)
    return msg