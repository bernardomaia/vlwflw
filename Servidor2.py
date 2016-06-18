import socket
import threading
import struct
import atexit

import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


BIND_IP = '0.0.0.0'
BIND_PORT = 9001



class Servidor:
    listaClientes = []
    
    passiveConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    passiveConnection.bind(( BIND_IP, BIND_PORT))
    passiveConnection.listen(5)
    print"[*] Listening on %s:%d" % (BIND_IP, BIND_PORT)
    
    
    def __init__(self):
        atexit.register(self.fecharConexao)
        
        
        while 1:
            client, addr = self.passiveConnection.accept()
            print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()
    
    def handle_client(self, conexao):

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
            if (self.hasCliente(origem) == False):
                self.enviaOK(conexao, origem, seqNo, timestamp)
                self.listaClientes.append([origem, conexao])
                logging.info("Novo cliente. ID = %d %s", origem, str(conexao.getpeername())) 
            else:
                novoID = self.encontraIdDisponivel(origem)
                self.enviaOKnovoID(conexao, origem, seqNo, timestamp, novoID)
                self.listaClientes.append([novoID, conexao])
                logging.info("Novo cliente. ID = %d %s", novoID, str(conexao.getpeername()))
        
        tipo,origem,_,seqNo,timestamp,_,corpo = recebe()
        if (tipo == 1):
            self.listaClientes.remove([origem,conexao])
            print "Removi o cliente ", origem
    
        
    
    
    
    def hasCliente(self, c):
        for [id, socket] in self.listaClientes:
            if (id == c):
                return True
        return False
    
    def enviaOK(self, conexao, idCliente, seqNo, timestamp):
            conexao.send(self.traduzirMensagem(3,0,idCliente,seqNo,timestamp,""))
    
    def enviaOKnovoID(self, conexao, idCliente, seqNo, timestamp, novoID):
            conexao.send(self.traduzirMensagem(8,0,idCliente,seqNo,timestamp,str(novoID)))
    
    def traduzirMensagem(self,tipo, origem, destino, seqNo, timestamp, corpo):
        pacote = struct.pack('!HHHIIH', tipo, origem, destino, seqNo, timestamp, len(corpo))
        pacote += corpo
        return pacote
    
    def encontraIdDisponivel(self, original):
        # EMISSOR
        if (original < 1000):
            current = 1
            while (self.hasCliente(current) and current < 1000):
                current += 1
            return current
        #EXIBIDOR
        else:
            current = 1000
            while (self.hasCliente(current)):
                current += 1
            return current
        
    def fecharConexao(self):
        logging.info("Estou fechando a conexao. Auf Wiederhoren!")
        self.passiveConnection.close()
     
    
    
if __name__ == '__main__':
    Servidor()