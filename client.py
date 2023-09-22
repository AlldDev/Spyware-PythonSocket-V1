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

_PORT = int(sys.argv[1])

if __name__ == "__main__":
    sel = None
    soc = None
    key = None
    mask = None
    events = None

    send_file = None

    # Iniciando nosso seletor padrão e Configurando o Socket
    sel = selectors.DefaultSelector()
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setblocking(False)
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
                    print('Conexão com o servidor fechada...')
                    sys.exit()
                    
                    
                    
                # Tratando se for msg
                if entry[:3] == 'msg':
                    print('Servidor >>> {}'.formatentry[3:]))
                    # soc.send(('Mensagem Recebida! >>> {}'.format(entry[3:])).encode())
                    
                    
                    
                # Tratando se for Comando
                elif entry[:3] == 'cmd':
                    
                    
                    
                    # Reconhece o cmd copiar
                    if entry[3:6] == 'cpy':
                        caminho_arq = os.path.join(os.getcwd(), entry[6:len(entry)-1])
                        send_file = [open(caminho_arq, 'rb'), os.path.getsize(caminho_arq), True]

                        
                        
                    # Retorna a pasta em que estamos
                    elif entry[3:] == 'cd':
                        soc.send(os.getcwd().encode())
                        continue
                    
                    
                    
                    # Aqui ele navega nas pastas como se fosse o cliente 
                    elif entry[3:5] == 'cd':
                        os.chdir(entry[6:len(entry)-1])
                        soc.send((os.getcwd()).encode())
                        
                        
                        
                    # Aqui ele trata tudo que sobrou como um comando
                    elif len(entry) > 0:
                        saida = subprocess.getoutput(entry[3:])
                        soc.sendall(saida.encode())
                        
                        
                        
            # Se o sistema estiver pronto para gravar ou enviar arquivos            
            elif mask & selectors.EVENT_WRITE:
                if send_file:
                    if send_file[2]:
                        print('Enviando tamanho ... {}'.format(send_file[1]))
                        key.fileobj.send('FIL{:03d}'.format(send_file[1]).encode())
                        # time.sleep(1e-9)
                        send_file[2] = False

                    # Se o tamanho do arq for maior que 0
                    elif send_file[1] > 0:
                        # Se o tamanho for maior que 512
                        if send_file[1] > 512:
                            print('Enviando pedaço ... 512')
                            data = send_file[0].read(512)
                            m = 'FIL{:03d}'.format(len(data)).encode()
                            m = m + data
                            key.fileobj.send(m)
                            # time.sleep(1e-9)
                            # Removendo o pedaço enviado do tamanho do vetor
                            send_file[1] = send_file[1] - 512
                            
                        # se for menor envia direto
                        else:
                            print('Enviando pedaço ... {}'.format(send_file[1]))
                            data = send_file[0].read(send_file[1])
                            m = 'FIL{:03d}'.format(len(data)).encode()
                            m = m + data
                            key.fileobj.send(m)
                            # time.sleep(1e-9)
                            send_file[1] = 0

                        if send_file[1] == 0:
                            send_file[0].close()
                            print('Arquivo Enviado!')
                        
        #print("[{}] {}".format(key.fileobj, entry))
        #soc.send(entry.encode())
