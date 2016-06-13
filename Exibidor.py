import socket

HOST = '0.0.0.0'
PORT = 9090
DATA = 'Hello server'
ID = 10

def tcp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(( HOST, PORT ))
     
    while 1:
        client.send(raw_input())
        print client.recv(4096)
        print "\n"
        
if __name__ == '__main__':
    tcp_client()