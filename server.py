import socket
import selectors
import sys

_HOST = 'localhost'
_PORT = 9997
_MAX_MSG_SIZE = 8192

if __name__ == "__main__":
    sel = None
    soc = None
    key = None
    mask = None
    events = None
    addr = None
    conn = None
    resto = None
    #data_rec = None

    recv_files = [None, None]

    # Iniciando o seletor como padrão
    sel = selectors.DefaultSelector()

    # AF_INET: Formato (Host, Port)
    # SOCK_STREAM: TCP
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Fazendo a ligação do Socket com o endereço
    soc.bind((_HOST, _PORT))

    soc.listen(100)

    # Setando como não bloqueante
    soc.setblocking(False)

    # Regsitrando nosso socket com o selector
    sel.register(soc, selectors.EVENT_READ)

    # Registrando o 'stdin' (usuário digitando) com o selector
    sel.register(sys.stdin.fileno(), selectors.EVENT_READ)

    #################################
    # Loop Principal
    #################################
    while True:
        events = sel.select()

        for key, mask in events:

            # Recebendo nova conexão
            if key.fileobj == soc:
                conn, addr = soc.accept()
                conn.setblocking(False)
                sel.register(conn, selectors.EVENT_READ)
                print('Nova conexão em {}'.format(key.fileobj))
                
            # Se o Usuario Digitou Algo
            elif key.fileobj == sys.stdin.fileno():
                # Coloca oque ele digitou aqui... (substitui o input)
                entry = sys.stdin.readline()

                if entry[:4] == '/msg':
                    conn.send(('msg' + entry[5:]).encode())

                elif entry[:4] == '/cmd':
                    # Caso for comando de Copiar
                    if entry[5:8] == 'cpy':
                        conn.send(('cmdcpy' + entry[9:]).encode())
                        name_arq = (entry[9:len(entry)-1])
                        print(name_arq)
                        # Abrindo arquivo com mesmo nome e guardando na posição 1
                        recv_files[0] = open(name_arq, 'w+')
                        
                        recv_files[1] = None
                        
                        #with open(name_arq, 'wb') as file:
                        #    fparts = int(conn.recv(1024).decode())
                        #    while fparts > 0:
                        #        print('Recebendo...')
                        #        arqv = conn.recv(1024)
                        #        if not arqv:
                        #            break
                        #        file.write(arqv)
                        #        fparts -= 1
                                
                        #    print('{} Recebido...'.format(entry[9:]))
                        #    continue
                        
                    else:
                        # Se for comandos "normais"        
                        conn.send(('cmd' + entry[5:]).encode())
                    
            else:
                # Recebendo os Dados
                data = key.fileobj.recv(_MAX_MSG_SIZE)
                data = data.decode()

                if data[:3] == 'FIL':
                    if recv_files[1] == None:

                        if data.find('FIL', 3) == -1:
                            recv_files[1] = int(data[3:])
                        else:
                            recv_files[1] = int(data[3:data.find('FIL', 3)])
                        
                            pos = data.find('FIL', 3) + 3
                            tam = int(data[pos:pos+3])
                            if len(data[pos+3:]) == tam:
                                chunk = data[pos+3:]
                                recv_files[0].write(chunk)
                                recv_files[1] -= tam
                            elif len(data[pos+3:]) > tam:
                                chunk = data[pos+3:pos+3+tam]
                                recv_files[0].write(chunk)
                                recv_files[1] -= tam
                                data = data[pos+3+tam:]
                        
                                while len(data) > 0:
                                    tam = int(data[3:6])
                                    if len(data[6:]) >= tam:
                                        dados = data[6:6+tam]
                                        data = data[6+tam+1:]
                                        recv_files[0].write(dados)
                                    else:
                                        falta = tam - len(data[6:])
                                        resto = key.fileobj.recv(falta)
                                        dados = data[6:] + resto
                                        recv_files[0].write(dados)
                                        data = ''

                                    recv_files[1] -= tam
                                continue


                            
                            else:
                                falta = tam - len(data[pos+3:]
                                resto = key.fileobj.recv(falta)
                                r
                            chunk = data[pos:]
                            recv_files[0].write(chunk)
                            recv_files[1] = recv_files[1] - len(chunk)

                            if recv_files[1] <= 0:
                                recv_files[0].close()
                                print('Arquivo recebido')
                    else:
                        print('Recebendo pedaço do arquivo ...')

                        pos = 3
                        while data.find('FIL', pos) != -1:
                            chunk = data[pos:data.find('FIL', pos)]
                            recv_files[0].write(chunk)
                            recv_files[1] = recv_files[1] - len(chunk)
                            pos = data.find('FIL', pos) + 3

                        chunk = data[pos:]
                        recv_files[0].write(chunk)
                        recv_files[1] = recv_files[1] - len(chunk)

                        print('missing: {}'.format(recv_files[1]))
                        
                        if recv_files[1] <= 0:
                            recv_files[0].close()
                            print('Arquivo recebido')
                else:
                    print('###################################\n'
                          '>>> {}\n'
                          '###################################\n'
                          '{}'.format(addr, data))
