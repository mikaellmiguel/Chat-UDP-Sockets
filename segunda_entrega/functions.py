import crcmod

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

