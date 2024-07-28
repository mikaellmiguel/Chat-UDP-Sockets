# Arquivo que contém váriaveis e constantes que serão usadas tanto pelo cliente quanto pelo servidor

# Constantes 

HEADER_SIZE = 4                             # Tamanho do HEADER
BUFFER_SIZE = 1024                          # Tamanho do Buffer
PAYLOAD_SIZE = BUFFER_SIZE-HEADER_SIZE      # Tamanho máximo de payload por pacote

TIMEOUT = 0.300 # Tempo de 300 MS até reenviar o pacote


# Variaveis
ackRecive = False  # Utilizada para aletar a chegada do ACK e parar o temporizador

