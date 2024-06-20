import socket
import queue
import threading
import os    # Para Remoção de Arquivos TXT quando o usuário sair da sala
import datetime   # Obtenção da data e tempo do servidor para repasse da mensagem para os cliente.
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
            print(f'Mensagem completa recebida de {clientAddr}')
        # Se tiver sido enviando uma flag para entrada/saída do usuário da sala
        elif mensagem.startswith("LOGIN:") or mensagem.startswith("LOGOUT:"):
            filaMsg.put((mensagem, clientAddr))

        # Adicionando o fragmento de mensagem na váriavel que armazará a mensagem completa
        else:
            fullMensage += mensagem

# Criando uma Thread para receber as mensagens
threadReceber = threading.Thread(target=receberMsg)
threadReceber.start()

def enviarMsg():
    while True:
        while not filaMsg.empty():
            mensagem, clienteAddr = filaMsg.get()  # Obtendo a mensagem e o endereço da mensagem a ser enviada
          
            # Quando o usuário que se conectar na sala.
            if  mensagem.startswith("LOGIN:"):
                username = mensagem[6:]
                clientes[clienteAddr] = username  # Adicionando o endereço e usuário no dicionário de clientes
                sendToAll(f"{username} entrou na Sala", clientes) # Enviando a mensagem de entrada

            
            # Quando o usuário coloca o BYE e envia a flag de quer ser desconctado da sala
            elif mensagem.startswith("LOGOUT:"):
                username = clientes[clienteAddr] # Obtendo o username
                del clientes[clienteAddr] # Deletando do dicionários para parar de receber mensagens
                sendToAll(f"{username} saiu na Sala", clientes) # Enviando a mensagem de saída
                
                try:
                    os.remove(f'./primeira_entrega/dados/server/{username}.txt')  # Removendo os arquivos do usuário desconectado
                except:  # Caso o arquivo TXT não tenha sido Criado (Cenário que o Usuário se Conecta, não envia mensagem e sai da sala)
                    pass

            else:
                # Modificando a mensagem que deverá ser enviada (Inserido as informações requesitas)
                mensagemToSend = f'{clienteAddr[0]}:{clienteAddr[1]}/~{clientes[clienteAddr]}: {mensagem} {datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")}'

                sendToAll(mensagemToSend, clientes) # Enviando a mensagem para todos os clientes

# Função para enviar para todos que estiverem no chat
def sendToAll(mensagem:str, clientes:dict):

    mensagem = mensagem.encode('ISO-8859-1')

    for cliente in clientes:
        for i in range(0, len(mensagem), BUFFER_SIZE):
            socketServer.sendto(mensagem[i:i+BUFFER_SIZE], cliente)
        
        socketServer.sendto('<EOF>'.encode(), cliente)

# Criação da Thread para recibimento
threadEnviar = threading.Thread(target=enviarMsg)
threadEnviar.start()