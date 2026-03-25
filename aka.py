import socket ,os
import subprocess
import time

while True:
    try :
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(('127.0.0.1',8000))
        print('Connected')
        break
    except Exception as e:
        print(e)
        print('Wait to connect with server')
        time.sleep(5)
        
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
                print(f"\rsending : |{bar}|{send}",end='')
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

def IpNo(no,ips):
    for i ,item in enumerate(ips,start=1):
        if no==i:
            return item[0]
while True:
    all_ips=subprocess.run(['arp','-a'],capture_output=True,text=True)
    selected_ip=[i.split() for i in all_ips.stdout.splitlines() if 'dynamic'in i]
    for i,item in enumerate(selected_ip,start=1):
        print(i,item[0])
    choice=int(input('enter a choice'))
   
    if 0<choice<len(selected_ip[0][0]):
        ip=IpNo(choice,selected_ip)
        client.sendall(ip.encode().ljust(64,b' '))
                       
       
        
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
       
    elif choice==-1:
        break
    else :
        print('you entered wrong ip choice')   
client.close()