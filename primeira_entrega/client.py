import socket
import os   # Biblioteca utilizada para remoção de arquivos TXT

from functions import *

# Constantes
SERVER_ADDR = ('localhost', 12000)  # Endereço do Servidor (IP e Porta)
BUFFER_SIZE = 1024                  # Tamanho do Buffer

# Criação do SOCKET
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Armazena se o cliente está conectado a uma sala ou não
conectado = False
# Armazenará o nome do usuário
username = ''

# Loop que rodará o chat
while True:

    mensagem = input()  # Aguarda a entrada do usuário para enviar mensagem/conectar/sair da sala

    if conectado:

        # Quando o usuário quer se desconectar da sala
        if mensagem == 'bye':
            conectado = False  # alterando a váriavel que indica se o cliente está conectado

            # Envia uma mensagem para o servidor informando que o cliente está saindo da sala
            socketCliente.sendto(f"LOGOUT:{username}".encode(), SERVER_ADDR)
            
            try:
                os.remove(f'./primeira_entrega/dados/client/{username}.txt')  # Apagando o TXT associado ao usuário que saiu
           
            except:  # Caso o usuário e entre na sala e saia sem mandar mensagens (Não existirá arquivo txt).
                pass

        
        # Quando o usuário quer enviar uma mensagem para os outros usuários
        else:
           pass
           
           # IMPLEMENTAR A CONVERSÃO PARA TXT
           # IMPLEMENTAR A SEGMENTAÇÃO DE ACORDO COM O BUFFER SIZE
        
    else:
        
        # Quando o usuário quer entrar na sala
        if mensagem.startswith("hi, meu nome eh "):
            username = mensagem[16:]  # Obtendo o username
            conectado = True

            # Enviando uma flag para o servidor informando a entrada do usuário com seu username
            socketCliente.sendto(f"LOGIN:{username}".encode(), SERVER_ADDR)

        # Quando o usuário quer sair sem estar conectado
        elif mensagem == 'bye' and conectado == False:
            print("Você não está conectado a sala")

        else:
            print("Comando Inválido")