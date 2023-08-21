import socket
import selectors
import sys
import types
import subprocess
import os
import time
import math

_HOST = 'localhost'
_PORT = 9889
_MAX_MSG_SIZE = 4096

if __name__ == "__main__":
    sel = None
    soc = None
    key = None
    mask = None
    events = None

    # Iniciando o seletor como padrão
    sel = selectors.DefaultSelector()

    # AF_INET: Formato (Host, Port)
    # SOCK_STREAM: TCP
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Setando como não bloqueante
    soc.setblocking(False)

    # Conectando
    soc.connect_ex((_HOST, _PORT))

    sel.register(soc, selectors.EVENT_READ)

    while True:
        events = sel.select()

        for key, mask in events:
            # Recebendo oque foi enviado
            if mask & selectors.EVENT_READ:
                entry = key.fileobj.recv(_MAX_MSG_SIZE)
                entry = entry.decode()
                # Se não receber nada, fecha a conexão
                if not entry:
                    print("Fechando conexão: {}".format(key.fileobj))
                    sel.unregister(key.fileobj)
                    key.fileobj.close()
                    # continue
                    break

                # Se o cliente não fechou a conexão, podemos tratar a mensagem
                # Tratando se for msg
                if entry[:3] == 'msg':
                    print(entry[3:])
                    soc.send(('Mensagem Recebida! >>> {}'.format(entry[3:])).encode())

                # Tratando se for Comando
                elif entry[:3] == 'cmd':
                    # Reconhece o cmd copiar
                    if entry[3:6] == 'cpy':
                        caminho_arq = os.path.join(os.getcwd(), entry[6:len(entry)-1])
                
                        with open(caminho_arq, 'rb') as file:
                            # Dividindo o Arquivo
                            tam_arq = str(math.ceil(os.path.getsize(caminho_arq) / 512))
                            soc.send((tam_arq).encode())
                            while True:
                                data = file.read(512)
                                if not data:
                                    break
                                soc.send('FIL{}'.format(data))
                                print('Arquivo {} Enviado!'.format(entry[6:]))
                                continue
                
                    elif entry[3:] == 'cd':
                        soc.send(os.getcwd().encode())
                        continue
                    
                    elif len(entry) > 0:
                        saida = subprocess.getoutput(entry[3:])
                        print(saida)
                        soc.send(saida.encode())

                    elif entry[3:5] == 'cd':
                        print('Comando do Servidor >>> {}'.format(entry[6:]))
                        os.chdir(entry[6:len(entry)-1])
                        soc.send((os.getcwd()).encode())
        
        #print("[{}] {}".format(key.fileobj, entry))
        #soc.send(entry.encode())
