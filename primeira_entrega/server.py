import socket
import queue
import threading
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

# Função utilizada para receber as mensagens do cliente
def receberMsg():
    fullMensage = ''  # Irá armazenar a mensagem completa

    
    while True:
        mensagem, clientAddr = socketServer.recvfrom(BUFFER_SIZE)

        mensagem = mensagem.decode('ISO-8859-1')  # Decodificando o fragmento de mensagem
 
        if mensagem == "<EOF>":  # Quando for uma flag dizendo que o arquivo foi trasmitido
            
            caminho = converterToTxt(clientes[clientAddr], fullMensage, True) # Convertendo a mensagem em um arquivo TXT

            # Abrindo o arquivo TXT
            with open(caminho) as file:
                contentFile = file.read()
            
            # Inserido na fila o conteudo do arquivo TXT
            filaMsg.put((contentFile, clientAddr))
            fullMensage = ''  # Esvaziando a variável para a proxima mensagem
        
        # Se tiver sido enviando uma flag para entrada/saída do usuário da sala
        elif mensagem.startswith("LOGIN:") or mensagem.startswith("LOGOUT:"):
            filaMsg.put((mensagem, clientAddr))

        # Adicionando o fragmento de mensagem na váriavel que armazará a mensagem completa
        else:
            fullMensage += mensagem

# Criando uma Thread para receber as mensagens
threadReceber = threading.Thread(target=receberMsg)
threadReceber.start()

# Função para enviar para todos que estiverem no chat
def sendToAll(mensagem:str, clientes:dict):

    mensagem = mensagem.encode('ISO-8859-1')

    for cliente in clientes:
        for i in range(0, len(mensagem), BUFFER_SIZE):
            socketServer.sendto(mensagem[i:i+BUFFER_SIZE], cliente)
        
        socketServer.sendto('<EOF>'.encode(), cliente)