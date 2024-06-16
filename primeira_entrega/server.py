import socket
import queue
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