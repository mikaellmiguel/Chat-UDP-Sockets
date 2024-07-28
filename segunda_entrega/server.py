import socket
import queue
import threading
import os        # Para Remoção de Arquivos TXT quando o usuário sair da sala
import datetime   # Obtenção da data e tempo do servidor para repasse da mensagem para os cliente.
from functions import *

from commom import *

# Criação do SOCKET
socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServer.bind(('', 12000))

# Dicionário que armazenará os endereços e usernames dos clientes
clientes = {}

# Dicionário que armazena os números de sequência e Ack para se comunicar com cada cliente
clientesSeqAck = {}

# Exemplo de utilização do Dicionário Acima
# clienteSeqAck[Endereço do Cliente] = [SEQ_NUMBER, ACK_NUMBER]


# Fila que armazenará as mensagens que devem ser enviadas
filaMsg = queue.Queue()


# Função utilizada para receber as mensagens do cliente
def receberMsg():
    fullMensage = ''  # Irá armazenar a mensagem completa

    
    while True:
        mensagem, clientAddr = socketServer.recvfrom(BUFFER_SIZE)

        header = mensagem[:HEADER_SIZE]
        payload = mensagem[HEADER_SIZE:]

        # Inserindo o número de sequencia e ack do cliente no dicionário para comunicação
        if not clientesSeqAck.get(clientAddr):
            clientesSeqAck[clientAddr] = [0, 0]
 
        # Verificando se o pacote não é corrompido
        if isCorrupt(header, payload):
            print("FAILED: PACOTE CORROMPIDO")
        
        else:

            payload = payload.decode('ISO-8859-1')  # Decodificando o payload

            seq, ack, _ = struct.unpack('!BBH', header) # Desempacotando os elementos do header
            
            # Se tiver payload e for o número de sequência esperado
            if payload and seq == clientesSeqAck[clientAddr][1]:

                # Se começar com a TAG Login
                if payload.startswith("LOGIN:"):
                    # Colocar o usuário no dicionáio de clientes
                    clientes[clientAddr] = payload[6:]
                    
                # Pritando que o pacote foi recebido
                print(f"INFO: PACOTE RECEBIDO DE {clientAddr} | SEQ = {seq} | PAYLOAD = '{payload}'")

                # Criando e enviando o ack para confirmar o recebimento
                pacote = makeAck(clientesSeqAck[clientAddr][0],clientesSeqAck[clientAddr][1])
                socketServer.sendto(pacote, clientAddr)

                # Pritando que o ACK foi enviado
                print(f"INFO: ACK {clientesSeqAck[clientAddr][1]} ENVIADO PARA {clientAddr}")
                
                # Atualizando o ack que deverá ser enviado no próximo pacote
                clientesSeqAck[clientAddr][1] = 1 if  clientesSeqAck[clientAddr][1] == 0 else 0

                # Se for <EOF> o payload quer dizer que a mensagem chegou ao fim.
                if payload == "<EOF>":

                    # Criando o arquivo TXT para mensagem no lado do servidor
                    caminhoTxt = converterToTxt(clientes[clientAddr], fullMensage, isServer=True)
                    
                    # Pritando que a mensagem completa foi recebida
                    print(f"INFO: MENSAGEM COMPLETA RECEBIDA DE {clientAddr} SALVO EM: {caminhoTxt}\n")
                    filaMsg.put((caminhoTxt, clientAddr))
                    
                    # Esvaziando o buffer para receber uma nova mensagem
                    fullMensage = ''
                    

                else:

                    fullMensage += payload

            # Se o sequence number do pacote for diferente do ACK que é para ser enviado, é possivel se uma retransmissão
            elif payload and seq != clientesSeqAck[clientAddr][1]:
                makeAck(clientesSeqAck[clientAddr][0], seq)  # Enviando o ACK do pacote recebido

            # Se a mensagem não tiver, um payload é um ack
            else:
                
                # Se o ack for realmente o esperado (Número de Sequência do último envio)
                if ack == clientesSeqAck[clientAddr][0]:

                    print(f"INFO: ACK {ack} RECEBIDO COM SUCESSO")

                    commom.ackRecive = True  # Informar o recebimento para parar o temporizador

                    # Trocando o próximo número de sequência a ser enviado
                    clientesSeqAck[clientAddr][0] = 1 if clientesSeqAck[clientAddr][0] == 0 else 0

                # Se for um ack para um número de sequência diferente do esperado
                elif not payload and ack != clientesSeqAck[clientAddr][0]:
                    print(f"FALIED: ACK NUMBER INCORRETO ({ack})")
                    # NÃO ESTOU FAZENDO NADA PORQUE EVENTUALMENTE O TIMER VAI ESTOURAR E REENVIAR O PACOTE



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