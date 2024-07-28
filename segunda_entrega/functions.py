import crcmod
import struct

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