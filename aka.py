import socket ,os
import subprocess


client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',8000))

def sendfile():
    file=input('file name')
    if os.path.exists(file):
        client.sendall(f'{os.path.basename(file)}|{os.path.getsize(file)}'.encode().ljust(64,b' '))
        send =0
        file_size=os.path.getsize(file)
        with open(file,'rb') as f:
            while chunk :=f.read(65536):
                client.sendall(chunk)
                send+=len(chunk)
                bar='█'*int((send/file_size)*100)+'-'*(100-int((send/file_size)*100))
                print(f"\rsending : |{bar}|",end='')
        print()
    else :
        print('file is not found')      
            
def sendmsg():
    msg =input('enter a massange')
    client.sendall(msg.encode())   
    print("massage sent")
    
    
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

while True:
    # ips=client.recv(64).decode()
    # print(ips)
    # print('For exit print -1')
    # choice=int(input('enter a choice'))
    # if 0<choice<len(ips):
    #     client.sendall(ips[ip-1])
        while True:
            a=input('what you wnat to send :\n1.file\n2.massage\n3.exit\n')
            client.sendall(a.encode())
            
            match a:
                case '1' :
                    sendfile()
                case '2' :
                    sendmsg()
                case '3' :
                    break
                case '4':
                    os.system('arp -a')
                case _ :
                    print('you entered wrong choice')
        break
    # elif choice==-1:
    #     break
    # else :
    #     print('you entered wrong ip choice')   
client.close()