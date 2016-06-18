import socket
import threading
import struct

BIND_IP = '0.0.0.0'
BIND_PORT = 9087

global listaClientes
listaClientes = []

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
            
            if (hasCliente(origem) == False):
                enviaOK(client_socket,origem, seqNo, timestamp)
                listaClientes.append([origem, client_socket])
                print "Novo cliente. ID = ", origem, client_socket.getpeername() 
            else:
                novoID = encontraIdDisponivel(origem)
                enviaOKnovoID(client_socket,origem, seqNo, timestamp, novoID)
                listaClientes.append([novoID, client_socket])
                print "Novo cliente. ID = ", novoID, client_socket.getpeername()
                    
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

def hasCliente(c):
    for [id, socket] in listaClientes:
        if (id == c):
            return True
    return False

def enviaOK(conexao, idCliente, seqNo, timestamp):
        conexao.send(traduzirMensagem(3,0,idCliente,seqNo,timestamp,""))

def enviaOKnovoID(conexao, idCliente, seqNo, timestamp, novoID):
        conexao.send(traduzirMensagem(8,0,idCliente,seqNo,timestamp,str(novoID)))

def traduzirMensagem(tipo, origem, destino, seqNo, timestamp, corpo):
    pacote = struct.pack('!HHHIIH', tipo, origem, destino, seqNo, timestamp, len(corpo))
    pacote += corpo
    return pacote

def encontraIdDisponivel(original):
    # EMISSOR
    if (original < 1000):
        current = 1
        while (hasCliente(current) and current < 1000):
            current += 1
        return current
    #EXIBIDOR
    else:
        current = 1000
        while (hasCliente(current)):
            current += 1
        return current
    

if __name__ == '__main__':
    tcp_server()