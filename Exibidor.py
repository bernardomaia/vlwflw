import socket
import struct
import time
import logging

import sys
import atexit
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

HOST = '0.0.0.0'
PORT = 9001

class Exibidor:
    ID = 0
    seqNo = 0
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.connect((HOST, PORT))
   
    
    def __init__(self):
        atexit.register(self.fecharConexao)
        self.enviaOI()
        self.esperaOK()
        self.emFuncionamento()
        
    
    def enviaOI(self):
        logging.info(str(self.conexao.getsockname())+": Mandei OI para o servidor.")
        envia(self.conexao,traduzirMensagem(0,self.ID,0,self.seqNo,int(time.time()),""))
        self.seqNo += 1
        
    def esperaOK(self):
        tipo,_,_,_,_,_,corpo = recebe(self.conexao)
        if (tipo == 3):
            logging.info(str(self.conexao.getsockname())+": Recebi OK, ID continua %d", self.ID)
        elif (tipo == 8):
            self.ID = int(corpo)
            logging.info(str(self.conexao.getsockname())+": Recebi OK, ID novo %d", self.ID)
        return
        
    def emFuncionamento(self):
        logging.info("EM FUNCIONAMENTO: EMISSOR %d", self.ID)
        while 1:
            tipo,origem,_,_,_,_,corpo = recebe(self.conexao)
            
            #recebeu MSG
            if (tipo == 2):
                print "Emissor "+str(origem)+" diz: "+corpo
           
            #recebeu OKQEM    
            elif (tipo == 6):
                print "**** Clientes conectados no servidor ****"
                clientes = corpo.split()
                clientes.sort()
                emissores = filter(lambda x: x < 1000, clientes)
                exibidores = filter(lambda x: x >= 1000, clientes)
                print "Emissores: ", emissores
                print "Exibidores: ", exibidores
        
    def fecharConexao(self):
        print "fechando conexao"
        envia(self.conexao,traduzirMensagem(1, self.ID, 0, self.seqNo, int(time.time()), ""))
        logging.info("Enviei FLW para o servidor.")
#         tipo,_,_,seqNo2 = recebe(self.conexao)
#         while (tipo != 3 and seqNo2 != self.seqNo):
#             tipo,_,_,seqNo2 = recebe()
#         logging.info("Recebi OK. Estou fechando a conexao. Auf Wiederhoren!")
        self.conexao.close()

    
    
def traduzirMensagem(tipo, origem, destino, seqNo, timestamp, corpo):
    pacote = struct.pack('!HHHIIH', tipo, origem, destino, seqNo, timestamp, len(corpo))
    pacote += corpo
    return pacote

def envia(conexao,data):
        conexao.send(data)

def recebe(conexao):
        resposta = conexao.recv(struct.calcsize('!HHHIIH'))
        if (len(resposta) > 0):
            tipo, origem, destino, seqNo, timestamp, tamanho = struct.unpack('!HHHIIH', resposta)
            corpo = ""
            if (tamanho > 0):
                corpo = conexao.recv(tamanho)
            return tipo, origem, destino, seqNo, timestamp, tamanho, corpo
        
if __name__ == '__main__':
    Exibidor()
        
    
