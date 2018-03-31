import sys
import socket
import select

def main():
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    IP , PORT = sys.argv[1] , int(sys.argv[2])
    sock.connect((IP,PORT))
    while True:
        sockList = [sys.stdin , sock]
        read , write , error   = select.select(sockList,[],[])
        for s in read:
            if s == sock:
                message = s.recv(2048)
                print(message.decode('utf-8'))
            else:
                message = sys.stdin.readline()
                sock.send(message.encode('utf-8'))
                sys.stdout.write("(You):")
                sys.stdout.write(message)
                sys.stdout.flush()
    sock.close()





if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage : Script IP Port')
        exit()
    main()
