import socket
import struct
import time
import logging

import sys
import atexit
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

HOST = '0.0.0.0'
PORT = 9089
ID = 0
SEQ_NO = 0



def exibidor():
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.connect((HOST, PORT))
    
    
        

    def traduzirMensagem(tipo, origem, destino, seqNo, timestamp, corpo):
        pacote = struct.pack('!HHHIIH', tipo, origem, destino, seqNo, timestamp, len(corpo))
        pacote += corpo
        return pacote
    
    def enviaOI():
        logging.info(str(conexao.getsockname())+": Mandei OI para o servidor.")
        envia(traduzirMensagem(0,0,0,SEQ_NO,int(time.time()),""))
        
    def esperaOK():
        global ID
        tipo,_,_,_,_,_, corpo = recebe()
        if (tipo == 3):
            logging.info(str(conexao.getsockname())+": Recebi OK, ID continua %d", ID)
        elif (tipo == 8):
            ID = int(corpo)
            logging.info(str(conexao.getsockname())+": Recebi OK, ID novo %d", ID)
        return
    
    def envia(data):
        conexao.send(data)
        global SEQ_NO
        SEQ_NO += 1
        
    def recebe():
        resposta = conexao.recv(struct.calcsize('!HHHIIH'))
        if (len(resposta) > 0):
            tipo, origem, destino, seqNo, timestamp, tamanho = struct.unpack('!HHHIIH', resposta)
            corpo = ""
            if (tamanho > 0):
                corpo = conexao.recv(tamanho)
            return tipo, origem, destino, seqNo, timestamp, tamanho, corpo
        
        
    def emFuncionamento():
        logging.info("EM FUNCIONAMENTO: EMISSOR %d", ID)
        while 1:
            tipo,origem,_,_,_,_,corpo = recebe()
            
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
        
    def fecharConexao():
        envia(traduzirMensagem(1, ID, 0, SEQ_NO, int(time.time()), ""))
        logging.info("Enviei FLW para o servidor.")
        tipo,_,_,seqNo = recebe()
        while (tipo != 3 and seqNo != SEQ_NO):
            tipo,_,_,seqNo = recebe()
        logging.info("Recebi OK. Estou fechando a conexao. Auf Wiederhoren!")
        conexao.shutdown()
        conexao.close()
    
    
    
    enviaOI()
    esperaOK()
    emFuncionamento()
    fecharConexao()
    atexit.register(fecharConexao())
if __name__ == '__main__':
    exibidor()
        
    
