import socket
import threading
import struct
import atexit

import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


BIND_IP = '0.0.0.0'
BIND_PORT = 9000

global listaClientes
listaClientes = []

passiveConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_client(conexao):
    
    def recebe():
        resposta = conexao.recv(struct.calcsize('!HHHIIH'))
        if (len(resposta) > 0):
            tipo, origem, destino, seqNo, timestamp, tamanho = struct.unpack('!HHHIIH', resposta)
            corpo = ""
            if (tamanho > 0):
                corpo = conexao.recv(tamanho)
            return tipo, origem, destino, seqNo, timestamp, tamanho, corpo

    
    tipo,origem,_,seqNo,timestamp,_,corpo = recebe()
    if (tipo == 0):
        if (hasCliente(origem) == False):
            enviaOK(conexao, origem, seqNo, timestamp)
            listaClientes.append([origem, conexao])
            logging.info("Novo cliente. ID = %d %s", origem, str(conexao.getpeername())) 
        else:
            novoID = encontraIdDisponivel(origem)
            enviaOKnovoID(conexao, origem, seqNo, timestamp, novoID)
            listaClientes.append([novoID, conexao])
            logging.info("Novo cliente. ID = %d %s", novoID, str(conexao.getpeername()))
    
    tipo,origem,_,seqNo,timestamp,_,corpo = recebe()
    if (tipo == 1):
        listaClientes.remove([origem,conexao])
        print "Removi o cliente ", origem

    

def tcp_server():
    global passiveConnection
    passiveConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    passiveConnection.bind(( BIND_IP, BIND_PORT))
    passiveConnection.listen(5)
    print"[*] Listening on %s:%d" % (BIND_IP, BIND_PORT)

    while 1:
        client, addr = passiveConnection.accept()
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
    
def fecharConexao():
    global passiveConnection
    logging.info("Estou fechando a conexao. Auf Wiederhoren!")
    passiveConnection.close()
 
atexit.register(fecharConexao())
    
if __name__ == '__main__':
    tcp_server()