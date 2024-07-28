import crcmod
import struct
import commom
import socket
import time

def converterToTxt(username, texto, isServer = False):

    if not isServer:
        caminho = f'./segunda_entrega/dados/client/{username}.txt'
    
    else:
        caminho  = f'./segunda_entrega/dados/server/{username}.txt'

    with open(caminho, "w") as file:
        file.write(texto)

    return caminho

def calcularChecksum(data:bytes):

    # Obtendo a função que que calcula o checksum CRC-16
    crc16 = crcmod.predefined.mkCrcFun("crc-16")
    
    # Calculando o Checksum
    checksum = crc16(data)

    return checksum


def criarPacote(msg:bytes, seq:int, ack:int):

    # Payload da mensagem a ser enviada
    payload = msg

    # Header sem o Checksum 
    pseudoHeader = struct.pack('!BB', seq, ack)

    # Calculando o checksum com as informações do cabeçalho e o payload
    checksum = calcularChecksum(pseudoHeader+payload)

    # Header de 4 Bytes (Seq - 1 Byte, Ack - 1 Byte, Checksum - 2 Bytes)
    header = struct.pack('!BBH', seq, ack, checksum)
    
    # Criando o pacote (Cabeçalho + Dados)
    pacote = header+payload

    return pacote  # Retornando o pacote já pronto para envio


def isCorrupt(header:bytes, payload:bytes):

    seq, ack, checksum = struct.unpack('!BBH', header)

    checksumChecked = calcularChecksum(struct.pack('!BB', seq, ack)+payload)

    return checksumChecked != checksum


def enviarMsg(msg:bytes, sock:socket.socket, addr:tuple, seq:int, ack:int):

    # Criando o Pacote para envio
    pacote = criarPacote(msg, seq, ack)

    # Armazenando o tempo no qual o pacote será enviado
    timeLastChunk = time.time()

    # Enviando o pacote
    sock.sendto(pacote, addr)

    # Enquanto não receber um ACK
    while not commom.ackRecive:

        # Caso passe do tempo definido para Timeout
        if timeLastChunk + commom.TIMEOUT < time.time():
            # Atualiza o tempo de envio do ultimo Pacote
            timeLastChunk = time.time()
            print("TIMER: TEMPO ESTOURADO - REENVIO")

            # Reenvia o mesmo pacote até chegar a confirmação
            sock.sendto(pacote, addr)

    # Zerando o ACK para a próximo envio
    commom.ackRecive = False

def makeAck(seq, ack):
    # Cria um pacote sem mensagem (S/payload) com o ACK do pacote confirmado
    return criarPacote(''.encode("ISO-8859-1"), seq, ack)

