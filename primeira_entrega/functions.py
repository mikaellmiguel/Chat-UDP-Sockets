def converterToTxt(username, texto, isServer = False):

    if not isServer:
        caminho = f'./primeira_entrega/dados/client/{username}.txt'
    
    else:
        caminho  = f'./primeira_entrega/dados/server/{username}.txt'

    with open(caminho, "w") as file:
        file.write(texto)

    return caminho