import socket
import os   # Biblioteca utilizada para remoção de arquivos TXT
import threading

from functions import *

# Constantes
SERVER_ADDR = ('localhost', 12000)  # Endereço do Servidor (IP e Porta)
BUFFER_SIZE = 1024                  # Tamanho do Buffer

# Criação do SOCKET
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Pritando os comandos que o usuário pode realizar
print("""Comando           \t\t Ação
hi, meu nome eh <username> \t Entrar na sala
bye                        \t Sair da sala\n""")


# Recepção de mensagens
def receberMsg():
    
    mensagemCompleta = '' # Armazenará a mensagem completa

    while True:
        try:

            mensagem, _ = socketCliente.recvfrom(BUFFER_SIZE)  # Recebendo o fragmento de mensagem

            mensagem = mensagem.decode('ISO-8859-1')  # Docodificando a mensagem
            
            if mensagem:
                if mensagem == "<EOF>":  # Se a mensagem for igual a flag <EOF> (fim da mensagem do usuáro)
                    print(mensagemCompleta)  # Pritando a mensagem para o o usário
                    mensagemCompleta = ''  # Esvaziando a variavel para armazenar outra
                
                else:
                    mensagemCompleta += mensagem  # Adicionando o pedaço da mensagem a mensagem completa


        except:
            pass

# criação da treading para recebimento de mensagens
threadReceber = threading.Thread(target=receberMsg)
threadReceber.start()

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

            print("""\nComando           \t\t Ação
hi, meu nome eh <username> \t Entrar na sala
bye                        \t Sair da sala\n""")


        
        # Quando o usuário quer enviar uma mensagem para os outros usuários
        else:
           # Convertendo a entrada em um arquivo TXT associado ao nome de usuário
            caminhoTxt = converterToTxt(username, mensagem)
            # Lendo o arquivo TXT como bytes
            with open(caminhoTxt, 'rb') as arquivoTxt:

                # FRAGMENTAÇÃO DE PACOTES
                # Enviando o arquivo em partes (chunks) do tamanho do BUFFER_SIZE
                while chunks:= arquivoTxt.read(BUFFER_SIZE):
                    socketCliente.sendto(chunks, SERVER_ADDR)
               

                # Informando para o servidor que a transimissão do arquivo terminou (EOF - End of File)
                socketCliente.sendto('<EOF>'.encode(), SERVER_ADDR)
        
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