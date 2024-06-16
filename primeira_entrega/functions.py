def converterToTxt(username, texto, isServer = False):

    if not isServer:
        caminho = f'./dados/client/{username}.txt'
    
    else:
        caminho  = f'./dados/server/{username}.txt'

    with open(caminho, "w") as file:
        file.write(texto)

    return caminho