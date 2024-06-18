import socket
import queue
from functions import *

# Tamanaho do Buffer
BUFFER_SIZE = 1024

# Criação do SOCKET
socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServer.bind(('', 12000))

# Dicionário que armazenará os endereços e usernames dos clientes
clientes = {}

# Fila que armazenará as mensagens que devem ser enviadas
filaMsg = queue.Queue()

# Função para enviar para todos que estiverem no chat
def sendToAll(mensagem:str, clientes:dict):

    mensagem = mensagem.encode('ISO-8859-1')

    for cliente in clientes:
        for i in range(0, len(mensagem), BUFFER_SIZE):
            socketServer.sendto(mensagem[i:i+BUFFER_SIZE], cliente)
        
        socketServer.sendto('<EOF>'.encode(), cliente)