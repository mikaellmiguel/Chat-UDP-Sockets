import socket
import os   # Biblioteca utilizada para remoção de arquivos TXT
import threading


from commom import *
from functions import *

# Constantes
SERVER_ADDR = ('localhost', 12000)  # Endereço do Servidor (IP e Porta)

# Criação do SOCKET
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seqToSend = 0  # Número de sequencia a ser enviado
ackToSend = 0  # Ack a ser enviado (Número de sequência esperado no recebimento)


# Pritando os comandos que o usuário pode realizar
print("""Comando           \t\t Ação
hi, meu nome eh <username> \t Entrar na sala
bye                        \t Sair da sala\n""")


# Recepção de mensagens
def receberMsg():

    global seqToSend, ackToSend   # Váriaveis globais que vão precisar ser usadas
    
    mensagemCompleta = '' # Armazenará a mensagem completa

    while True:
        try:
            
            pacote, _ = socketCliente.recvfrom(BUFFER_SIZE)  # Recebendo o fragmento de mensagem

            #print(pacote)

            header = pacote[:HEADER_SIZE]
            payload = pacote[HEADER_SIZE:]

            
            # Se o Pacote estiver Corrompido (Checksum que verifica)
            if isCorrupt(header, payload): 
                print("FAILED: PACOTE CORROMPIDO")

            # Se o Pacote não Estiver Corrompido
            else:

                seq, ack, _ = struct.unpack("!BBH", header)  # Desempacotando o Header
                
                # Se não tem payload é um ACK, se for do pacote que foi enviado ( Número Sequência do Pacote enviado)
                if not payload and ack == seqToSend:
                    
                    # Informando que o ACK Do pacote enviado foi recibido para parar o temporizador
                    commom.ackRecive = True

                    # Trocando o número de Sequência para o próximo pacote  
                    seqToSend = 1 if seqToSend == 0 else 0

                
                # Se for um ACK, mas não for do pacote enviado.
                elif not payload and ack != seqToSend:
                    pass 

                # Se o número de sequência do pacote for diferente do ack a ser enviado (Do seq number esperado) enviar um ACK (Possível ACK corrompido)

                elif seq != ackToSend:
                    socketCliente.sendto(makeAck(seqToSend, seq), SERVER_ADDR)  # Enviar o ACK novamente
                
                # Se for algum contéudo
                else:
                    payload = payload.decode("ISO-8859-1")  # Decodificando o payload

                    # Enviando o ACK confirmando o Recebimento
                    ack = makeAck(seqToSend, ackToSend)
                    socketCliente.sendto(ack, SERVER_ADDR)
                    
                    # Atualizando qual é o ACK que deve ser enviado no próximo pacote
                    ackToSend = 1 if ackToSend == 0 else 0

                    # Se a mensagem for a tag <EOF>, ou seja, é o fim da mensagem
                    if payload == "<EOF>":
                        # Pritando a mensagem completa
                        print(mensagemCompleta)
                        mensagemCompleta = ''  # Esvaziando o buffer de mensagem para a próxima mensagem

                    else:
                        # Armazenando os pedaços de mensagens até que a mensagem chegue por completo para ser exibida
                        mensagemCompleta += payload

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
            enviarMsg(f'LOGOUT:{username}'.encode("ISO-8859-1"), socketCliente, SERVER_ADDR, seqToSend, ackToSend)
            enviarMsg('<EOF>'.encode("ISO-8859-1"), socketCliente, SERVER_ADDR, seqToSend, ackToSend)
            
            # Restaurando as váriaveis ao estado inicial (Caso queira se conectar novamente ao server)

            seqToSend = 0

            ackToSend =0

            #socketCliente.sendto(f"LOGOUT:{username}".encode(), SERVER_ADDR)
            
            
            try:
                os.remove(f'./segunda_entrega/dados/client/{username}.txt')  # Apagando o TXT associado ao usuário que saiu
           
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
                while chunks:= arquivoTxt.read(PAYLOAD_SIZE):
                    enviarMsg(chunks, socketCliente, SERVER_ADDR, seqToSend, ackToSend)
               

                # Informando para o servidor que a transimissão do arquivo terminou (EOF - End of File)
                enviarMsg('<EOF>'.encode("ISO-8859-1"), socketCliente, SERVER_ADDR, seqToSend, ackToSend)
        
    else:
        
        # Quando o usuário quer entrar na sala
        if mensagem.startswith("hi, meu nome eh "):
            username = mensagem[16:]  # Obtendo o username
            conectado = True

            # Enviando uma flag para o servidor informando a entrada do usuário com seu username
            enviarMsg(f"LOGIN:{username}".encode("ISO-8859-1"), socketCliente, SERVER_ADDR, seqToSend, ackToSend)
            enviarMsg("<EOF>".encode("ISO-8859-1"), socketCliente, SERVER_ADDR, seqToSend, ackToSend)


        # Quando o usuário quer sair sem estar conectado
        elif mensagem == 'bye' and conectado == False:
            print("Você não está conectado a sala")

        else:
            print("Comando Inválido")