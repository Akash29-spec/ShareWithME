import socket
import threading
import subprocess
import os
clients=[]


def getfile(data):
    arr =data.recv(64).decode().strip().split('|')
    recive=0
    print(arr[1])
    with open(arr[0],'wb') as f:
        while recive<int(arr[1]):
            chunk=data.recv(65536)
            if not chunk :
                break
            f.write(chunk)
            recive+=len(chunk)
            bar='█'*int(((recive/int(arr[1])))*100)+'-'*(100-int(((recive/int(arr[1]))*100)))
            print(f"\rRecived : |{bar}|{recive}",end='') 
    return arr[0]
                   
def sendfile(file,conn):
    client.sendall(f'{file}|{os.path.getsize(file)}'.encode().ljust(64,b' '))
    send =0
    file_size=os.path.getsize(file)
    with open(file,'rb') as f:
        while chunk :=f.read(65536):
            client.sendall(chunk)
            send+=len(chunk)

            bar='█'*int((send/file_size)*100)+'-'*(100-int((send/file_size)*100))
            print(f"\rRecived : |{bar}|",end='')
            print('\n',client.recv(64).decode())           
    
def getmassage(data):
    print(data.recv(64).decode())
    data.sendall(b'recived')
    
def msgtoall(data,conn):
    print(data.recv(64).decode())
    data.sendall(b'recived')
    
def sendall(data,choice):
    if choice==1:
        file=getfile(data)
    elif choice ==2:
        getmassage(data)
    else:
        return
    
    for i in clients:
        if choice==1:
            threading.Thread(target=sendfile,args=(file,i[0]))
        elif choice ==2:
            threading .Thread(target=msgtoall,args=(data,i[0]))
        else :
            break
                     
        
def client(data,info):
    print('connected to ',info)
    clients.append((data,info))
    # result = subprocess.run(["arp","-a"], shell=True, capture_output=True, text=True)
    # dynamic=[i for i in result.stdout.splitlines() if dynamic in i]
    # ips=[]
  
    while True :
        metadata=data.recv(1).decode()
        
        match metadata :
            case '1':
                getfile(data)
            case '2':
                getmassage(data)
            case '3':
                print('client disconnected')
                break
    data.close()

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('0.0.0.0',8000))
print('listening...')
server.listen(3)

while True:
    data,info=server.accept()
    t1=threading.Thread(target=client,args=(data,info))
    t1.start()
    
     
