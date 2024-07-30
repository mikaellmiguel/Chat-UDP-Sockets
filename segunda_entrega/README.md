<div align="center">
<img src="https://github.com/mikaellmiguel/Chat-UDP-Sockets/assets/144696910/b2494c37-e120-4b6c-a1a9-f0988699ea77" />
</div>

<h1 align="center">Chat UDP - Programação de Sockets</h1> 
  <h3 align="center">Redes de Computadores - 2024.1 CIn/UFPE - Equipe 2 



<p align="center">
<br />
  <a href="https://github.com/mikaellmiguel/Chat-UDP-Sockets"><strong>Ir para o repositório »</strong></a>
<br />
</p>



<p align="center">
    Descrição: Segunda entrega - Chat UDP com segmentação de arquivos TXT e Transferência Confiavél (RDT 3.0)
</p>

<h3 align="center">Vídeo - Apresentação do Projeto - RDT (https://youtu.be/q2DL5qlqq1E)

<a href="https://youtu.be/q2DL5qlqq1E"><img src="https://github.com/user-attachments/assets/63abe145-daa5-4dcd-900b-56f4de6660aa" /></a>


## Requesitos Mínimos ⚠️
* Estar em um ambiente desktop 🖥️
* Ter o Python instalado
* Ter uma IDE com suporte ao Python Instalada

## Instalação de Bibliotecas
Caso não tenha, alguma dessas bibliotecas abaixo é necessário a instalação, para o funcionamento do projeto.

```{r, echo=FALSE, warning=FALSE}
pip install socket
pip install time
pip install queue
pip install crcmod
pip install datetime
pip install threading
```


## Organização do Codigo
Arquivo  | Função
:--------:| -------------
<a href="https://github.com/mikaellmiguel/Chat-UDP-Sockets/blob/main/segunda_entrega/client.py">cliente.py</a> | O arquivo cliente.py contém o codigo que deverá ser executado pelo dispositivo que é cliente (Usuário do chat)
<a href="https://github.com/mikaellmiguel/Chat-UDP-Sockets/blob/main/segunda_entrega/server.py">server.py</a>| O arquivo servidor.py contém o codigo que deverá ser executado pelo dispositivo que é servidor (recebe as mensagens em TXT e repassa para os clientes).
<a href="https://github.com/mikaellmiguel/Chat-UDP-Sockets/blob/main/segunda_entrega/functions.py">functions.py</a>| O arquivo possui as funções que serão utilizadas no projeto, tanto no lado do servidor quanto no lado do cliente.
<a href="https://github.com/mikaellmiguel/Chat-UDP-Sockets/blob/main/segunda_entrega/commom.py">commom.py</a>| O arquivo possui as váriaveis e constantes que são comuns ao servidor e ao cliente.
<a href="https://github.com/mikaellmiguel/Chat-UDP-Sockets/blob/main/segunda_entrega/dados">dados</a>| Pasta que irá armazenar os arquivos TXT que serão fragmentados e enviados, a mesma contém uma pasta espefíca para o TXT que será enviado pelo cliemte, e outra pasta que contém o TXT que será recebido pelo servidor.

## Instruções de uso 
* Clone o repositório e abra a pasta.
* Execute inicialmente o arquivo *server.py*, que iniciará o servidor da sala.
* Crie novos terminais e execute os clientes que enviarão e receberão mensagens.
* Nos clientes, siga os comandos abaixo para conectar/sair da sala.
* Conectado na sala, o cliente pode enviar as mensagens para outros clientes conectados.

*OBSERVAÇÃO* ⚠️: Não abra diretamente a pasta da segunda entrega, abra a pasta geral (Chat-UDP-Sockets) no VS Code e execute os codigos da pasta primeira entrega, caso contrário, irá dar problemas para salvar o arquivo TXT por não localizar a pasta.


### Comandos
Comando  | Ação
:--------:| -------------
hi, meu nome eh {username}| Conectar a sala.
bye|  Sair da sala.


## Ênfases
### Implementação do RDT 3.0
O RDT 3.0 (Reliable Data Transfer Protocol 3.0) é um protocolo de comunicação usado para garantir a entrega confiável de pacotes de dados em uma rede. É uma evolução do RDT 2.1 e lida com alguns problemas adicionais que não eram resolvidos pelas versões anteriores.

A implementação do RDT 3.0 nesse projeto é baseada no mecanismo de "Stop and Wait", ou seja, **sem o uso de pipeline**, e aqui estão os principais pontos sobre como ela funciona:

#### Conceito Básico do RDT 3.0 "Stop and Wait"
**Envio de Pacote:** O emissor envia um pacote e espera pela confirmação (ACK) do receptor antes de enviar o próximo pacote.  
  
**Confirmação (ACK):** O receptor envia uma mensagem de confirmação para o emissor, indicando que o pacote foi recebido corretamente.  
  
**OBSERVAÇÃO:** O emissor aguarda o ACK antes de enviar o próximo pacote. Diante disso, é necessário apenas um bit para armazenar o número de sequência e outro bit para armazenar o ACK (Podem assumir dois valores: 0 e 1)

#### Adição de Controle de Erros:
**Detecção de Erros:** O RDT 3.0 utiliza somas de verificação (checksums) para detectar erros nos pacotes e nas confirmações.    
  
**Reenvio de Pacotes:** Se o emissor não recebe um ACK dentro de um tempo específico (300ms no projeto), ele assume que o pacote  ou corrompido e retransmite o pacote. O emissor faz isso quantas vezes for necessário até que o ACK seja recebido. 

#### Controle de Tempo:
**Temporizadores:** O emissor define um temporizador para cada pacote enviado. Se o ACK não chega antes do tempo expirar, o emissor retransmite o pacote.  
 
**Time-out:** O tempo de espera é crucial para garantir que os pacotes não sejam retransmitidos prematuramente ou que não haja uma espera indefinida.


#### Ciclo de Comunicação: 
   
**Envio:** O emissor envia um pacote de dados e inicia um temporizador.

**Recepção:** O receptor recebe o pacote, verifica a soma de verificação e envia um ACK se o pacote estiver correto.

**Recebimento do ACK:** O emissor recebe o ACK e para o temporizador. Se o ACK não chegar a tempo, o emissor retransmite o pacote.

### Slides - Ações do Transmissor e Receptor

<div align="center">
<img src="https://github.com/user-attachments/assets/79b0ad1e-87bb-4772-a154-8892ca788916"/>
</div>

<div align="center">
<img src="https://github.com/user-attachments/assets/25291498-eee1-4ef0-b6d5-1df3b9f7f4aa"/>
</div>

### Funcionameto Prático

<div align="center">
<img src="https://github.com/user-attachments/assets/98e731d1-1399-4ed4-bd74-f55ee4dd22e2"/>
</div>
