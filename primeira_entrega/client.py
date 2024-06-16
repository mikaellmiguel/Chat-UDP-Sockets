import socket

# Constantes
SERVER_ADDR = ('localhost', 12000)  # Endereço do Servidor (IP e Porta)
BUFFER_SIZE = 1024                  # Tamanho do Buffer

# Criação do SOCKET
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)