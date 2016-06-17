import socket
import threading
import struct

BIND_IP = '0.0.0.0'
BIND_PORT = 9097

def handle_client(client_socket):
    while 1:
        request = client_socket.recv(struct.calcsize('!HHHIIH'))
        if (len(request) > 0):
            print "Recebi uma coisa do cliente ", client_socket.getpeername()
            tipo, origem, destino, seqNo, timestamp, tamanho = struct.unpack('!HHHIIH', request)
            print "Tipo: ", tipo
            print "Origem: ", origem
            print "destino: ", destino
            print "seqNo: ", seqNo
            print "timestamp: ", timestamp
            print "tamanho: ", tamanho
            
            if (tamanho > 0):
                corpo = client_socket.recv(tamanho)
                print "corpo: ", corpo
            print "\n\n"        
#         print "Tipo: " + tipo
#         print "[*] Received: " + request
#         client_socket.send('ACK')
#         if (request == "sair"):
#             client_socket.close()
#             return

def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(( BIND_IP, BIND_PORT))
    server.listen(5)
    print"[*] Listening on %s:%d" % (BIND_IP, BIND_PORT)

    while 1:
        client, addr = server.accept()
        print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == '__main__':
    tcp_server()