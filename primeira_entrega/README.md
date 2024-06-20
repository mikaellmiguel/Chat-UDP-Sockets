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
    Descrição: Primeira entrega - Chat UDP com segmentação de arquivos TXT através do uso de Sockets
</p>

## Requesitos Mínimos ⚠️
* Estar em um ambiente desktop 🖥️
* Ter o Python instalado
* Ter uma IDE com suporte ao Python Instalada


## Organização do Codigo
Arquivo  | Função
:--------:| -------------
<a href="https://github.com/mikaellmiguel/Chat-UDP-Sockets/blob/main/primeira_entrega/client.py">cliente.py</a> | O arquivo cliente.py contém o codigo que deverá ser executado pelo dispositivo que é cliente (Usuário do chat)
<a href="hhttps://github.com/mikaellmiguel/Chat-UDP-Sockets/blob/main/primeira_entrega/server.py">server.py</a>| O arquivo servidor.py contém o codigo que deverá ser executado pelo dispositivo que é servidor (recebe as mensagens em TXT e repassa para os clientes).
<a href="https://github.com/mikaellmiguel/Chat-UDP-Sockets/blob/main/primeira_entrega/functions.py">functions.py</a>| O arquivo possui as funções que serão utilizadas no projeto. Nesse caso, o arquivo na primeira entrega contém a função para conversão de string em TXT.
<a href="https://github.com/mikaellmiguel/Chat-UDP-Sockets/blob/main/primeira_entrega/functions.py">data</a>| Pasta que irá armazenar os arquivos TXT que serão fragmentados e enviados, a mesma contém uma pasta espefíca para o TXT que será enviado pelo cliemte, e outra pasta que contém o TXT que será recebido pelo servidor.

## Instruções de uso 
* Clone o repositório e abra a pasta.
* Execute inicialmente o arquivo *server.py*, que iniciará o servidor da sala.
* Crie novos terminais e execute os clientes que enviarão e receberão mensagens.
* Nos clientes, siga os comandos abaixo para conectar/sair da sala.
* Conectado na sala, o cliente pode enviar as mensagens para outros clientes conectados.

*OBSERVAÇÃO* ⚠️: Não abra diretamente a pasta da primeira entrega, abra a pasta geral (Chat-UDP-Sockets) no VS Code e execute os codigos da pasta primeira entrega, caso contrário, irá dar problemas para salvar o arquivo TXT por não localizar a pasta.


### Comandos
Comando  | Ação
:--------:| -------------
hi, meu nome eh {username}| Conectar a sala.
bye|  Sair da sala.


## Ênfases
<div align="center">
<img src="https://github.com/mikaellmiguel/Chat-UDP-Sockets/assets/144696910/43538bb5-e3e6-4d4c-8be0-d5db39d28261" />
</div>

<h3 align="center">Imagem 1 - Código da segmentação e Envio do TXT pelo Cliente</h3>


#
#
<div align="center">
<img src="https://github.com/mikaellmiguel/Chat-UDP-Sockets/assets/144696910/2097643c-3285-440c-bc4a-a9771266e923" />
</div>

<h3 align="center">Imagem 2 - Código do Recebimento do TXT Fragmentado (Servidor)</h3>
