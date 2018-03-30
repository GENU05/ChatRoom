import sys
import socket
import select

def main():
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    IP , PORT = sys.argv[1] , int(sys.argv[2])
    sock.connect((IP,PORT))
    while True:
        sockList = [sys.stdin , sock]
        read , write , error   = select.select(sockList,list(),list())
        for s in read:
            if s == sock:
                message = s.recv(2048)
                var = message.decode('utf-8')
                if len(var)!=0:
                    print(message.decode('utf-8'))


                # print('*')      #For Debugging
            message = sys.stdin.readline()
            if len(message)!=0:
                sock.send(message.encode('utf-8'))
                sys.stdout.write("(You):" + message)
                sys.stdout.flush()
    sock.close()





if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage : Script IP Port')
        exit()
    main()
