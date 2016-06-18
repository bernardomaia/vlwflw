import socket
import random
import struct
import time
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
HOST = '0.0.0.0'
PORT = 9087
DATA = 'Hello server'
global ID
ID = 0
global SEQ_NO
SEQ_NO = 0

def exibidor():
    global conexao
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.connect((HOST, PORT))
    
    enviaOI()
    esperaOK()
    
    emFuncionamento()
    
        

def traduzirMensagem(tipo, origem, destino, seqNo, timestamp, corpo):
    pacote = struct.pack('!HHHIIH', tipo, origem, destino, seqNo, timestamp, len(corpo))
    pacote += corpo
    return pacote

def enviaOI():
    logging.info(str(conexao.getsockname())+": Mandei OI para o servidor.")
    envia(traduzirMensagem(0,0,0,SEQ_NO,int(time.time()),""))
    

def esperaOK():
    global ID
    tipo, origem, destino, seqNo, timestamp, tamanho, corpo = recebe()
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
    print "em funcionamento"
    
if __name__ == '__main__':
    exibidor()
    

    
    
# data=pack('!BBBBHHII', P2P_h.version, P2P_h.ttl, P2P_h.msgType, P2P_h.reserved, P2P_h.sendPort, P2P_h.payloadLength, P2P_h.ipSrc, P2P_h.messageId) #your current header
# data+= pack("!I",len(body)) #assumes len(body) fits into a integer
# data+= body #assumes body is a string
# socket.send(data)