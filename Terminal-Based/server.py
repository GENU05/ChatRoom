import socket
import threading
import sys
import select


connections = []    #active clients

def new_client(con,addr):
    try:
        pass
        # con.send('Welcome\n'.encode('utf-8'))
        # broadcast(' Joined\n'.encode('utf-8'),con,addr[0])
    except:
        pass
    while True:
         try:
             message = con.recv(2048) #max size of message 2048
             if message:
                 print("(" , addr[0] , ") : " , message.decode('utf-8'))
                 broadcast(message,con,addr[0])
             else:
                 remove(con) #Broken connection ==> Terminate
                 print("Removing : " , addr[0])
                 message = ' left \n'
                 broadcast(message.encode('utf-8'),con,addr[0])
                 return 0
         except:
            continue

def broadcast(message , con , addr):
    global connections
    outbox = '(' + addr +') ' + message.decode('utf-8')     #Its a string
    for clients in connections:
        if clients != con:
            try:
                clients.send(outbox.encode('utf-8'))
            except:
                clients.close()
                remove(clients)
def remove(con):
    if con in connections:
        connections.remove(con)
    return 0

def main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)     #TCP IPv4/6
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    IP , PORT = sys.argv[1] , int(sys.argv[2])
    sock.bind((IP,PORT))
    sock.listen(100)  # 100 connection at a time

    while True:
        con , addr = sock.accept()
        connections.append(con)
        print(addr[0] + " Joined")
        conThread = threading.Thread(target=new_client,args=(con,addr))
        conThread.deamon=True  #CAn close program even if Thread is running
        conThread.start()

    con.close()
    sock.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage : Script IP PORT")
        exit()
    print('Server Up and Running')
    main()
