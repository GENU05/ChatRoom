import socket
import threading
import sys
import select


connections = []    #active clients

def new_client(con,addr):
    try:
        con.send(bytes('Welcome'))
    except:
        pass
    while True:
         try:
             message = con.recv(2048) #max size of message 2048
             if message:
                 print("(" , addr[0] , ") : " , message)
                 broadcast(message,con,addr[0])
             else:
                remove(con) #Broken connection ==> Terminate
                print("Removing : " , addr[0])
                return 0
         except:
            # print('*')      #For Debbugin purpose
            continue
def broadcast(message , con , addr):
    global connections
    for clients in connections:
        #print('#')        #For Debbuging
        if clients != con:
            try:
                outbox = '('+addr+') ' + message
                clients.send(str.encode(outbox))
                print('!')
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
    sock.listen(10)  # 1 connection at a time

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
