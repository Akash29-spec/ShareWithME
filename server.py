import socket
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget,
    QTextEdit, QLineEdit, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt
import os
clients=[]


def getfile(data):
    arr =data.recv(256).decode().strip().split('|')
    print(arr)
    recive=0
    print(arr)
    with open(arr[0],'wb') as f:
        while recive<int(arr[1]):
            chunk=data.recv(1024*1024)
            if not chunk :
                break
            f.write(chunk)
            recive+=len(chunk)
            bar='█'*int(((recive/int(arr[1])))*100)+'-'*(100-int(((recive/int(arr[1]))*100)))
            print(f"\rRecived : |{bar}|{recive}",end='') 
    return arr[0]
                   
def sendfile(data,ip):
    conn=None
    for i in clients:
        if i[1][0]==ip:
            conn=i[0]
            conn.sendall(data.recv(64))
            while True:
                d=data.recv(65536)
                conn.sendall(d)
                if not d:
                    break
    getfile(data)
    
                     

    
def getmassage(data):
    print(data.recv(64).decode())
    data.sendall(b'recived')
                   
        
def client(data,info):
    print('connected to ',info)
    clients.append((data,info))
    ip=data.recv(64).decode().strip()
    
    while True :
        metadata=data.recv(1).decode()
        
        match metadata :
            case '1':
                if ip==socket.gethostbyname(socket.gethostname()):
                    getfile(data)
                sendfile(data,ip)   
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
    
     
