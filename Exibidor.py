import socket
import random
import struct
import time

HOST = '0.0.0.0'
PORT = 9097
DATA = 'Hello server'
global SEQ_NO


def exibidor():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(( HOST, PORT ))
    
    SEQ_NO = 0
    ID = random.randint(1, 999)
    
   
    # envia OI
    data = traduzirMensagem(0,ID,0,SEQ_NO,int(time.time()),"") 
    client.send(data)
    SEQ_NO += 1
    
    # envia MSG = "Esta e uma mensagem."
    data = traduzirMensagem(2,ID,0,SEQ_NO,int(time.time()),"Esta e uma mensagem.") 
    client.send(data)
    SEQ_NO += 1
    # recebe OK do servidor
        

def traduzirMensagem(tipo, origem, destino, seqNo, timestamp, corpo):
    pacote = struct.pack('!HHHIIH', tipo, origem, destino, seqNo, timestamp, len(corpo))
    pacote += corpo
    return pacote

if __name__ == '__main__':
    exibidor()
    

    
    
# data=pack('!BBBBHHII', P2P_h.version, P2P_h.ttl, P2P_h.msgType, P2P_h.reserved, P2P_h.sendPort, P2P_h.payloadLength, P2P_h.ipSrc, P2P_h.messageId) #your current header
# data+= pack("!I",len(body)) #assumes len(body) fits into a integer
# data+= body #assumes body is a string
# socket.send(data)