import socket
import selectors
import sys

_HOST = 'localhost'
_PORT = 9997
_MAX_MSG_SIZE = 8192

_PORT = int(sys.argv[1])

if __name__ == "__main__":
    sel = None
    soc = None
    key = None
    mask = None
    events = None
    addr = None
    conn = None
    resto = None

    recv_files = [None, None]

    # Iniciando o seletor como padrão
    sel = selectors.DefaultSelector()
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((_HOST, _PORT))
    soc.listen(100)
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
                data = sys.stdin.readline() # Substitui o input (bloqueante)
                
                if data[:4] == '/msg':
                    conn.send(('msg' + data[5:]).encode())
                    
                elif data[:4] == '/cmd':
                    if data[5:8] == 'cpy':
                        conn.send(('cmdcpy' + data[9:]).encode())
                        name_arq = (data[9:len(data)-1])
                        print(name_arq)
                        # Abrindo arquivo com mesmo nome e guardando na posição 1
                        recv_files[0] = open(name_arq, 'wb')
                        recv_files[1] = None
                    else:
                        # Se for comandos "normais"        
                        conn.send(('cmd' + data[5:]).encode())
                        
            # Se não foi digitado nada, ele recebe as Respostas do cliente aqui
            else:
                # Recebendo os Dados
                data = key.fileobj.recv(_MAX_MSG_SIZE)
                
                ################LOG##################
                #arq = open('log.txt', 'wb')
                #arq.write(data)
                #print(len(data.decode()))
                #####################################
                
                code = data[:3]
                code = code.decode()
                # print('data recebida > {}'.format(data.decode()))
                # print('code > {}\n'.format(code))
                
                # data_bytes = data
                # data = data.decode()
                # print(data)
                
                if code == 'FIL':
                    pos = 3
                    if recv_files[1] == None:
                        while True:
                            try:
                                c = int(data[pos:].decode())
                                pos += 1
                            except:
                                break;
                            
                        tam = data[3:pos].decode()
                        tam = int(tam)
                        print('Tam. {}'.format(tam))
                        print('Pos. {}'.format(pos))
                        # print('Data[pos:] > START{}END\n'.format(data[pos:].decode()))
                        
                        
                        
                        if len(data[pos:]) == 0:
                            recv_files[1] = tam
                            print('O Tam. veio sozinho >>>{}\n'.format(tam))
                            
                        # Se veio mais algum junto ! tratar depois
                        else:
                            recv_files[1] = tam
                            print('Tamanho veio com mais algo!')
                            # print('data antes do pos > {}'.format(data.decode()))
                            pos = data[3+tam:]
                            print('pos > {}\n'.format(pos))
                            code = data[pos:pos+3]
                            data = data[pos:]
                            #recv_files[1] = int(data[3:data.find('FIL', 3)])
                            #print('Tam. Veio com mais algo!!!')
                            #pos = data.find('FIL', 3) + 3
                            #data = data[pos-3:]
                            #data_bytes = data_bytes[pos-3:]
                            
                            while len(data) > 0:
                                if code != 'FIL':
                                    print('Opss, Cortou errado!')
                                    # print(data.decode() + '\n')
                                    
                                # print(tam)
                                
                                if len(data[6:]) >= tam:
                                    chunk = data[6:6+tam]
                                    data = data[6+tam:]
                                    # data_bytes = data_bytes[6+tam:]
                                    recv_files[0].write(chunk)
                                else:
                                    falta = tam - len(data[6:])
                                    resto = key.fileobj.recv(falta)
                                    chunk = data[6:] + resto
                                    recv_files[0].write(chunk)
                                    data = ''
                                print('Final do While 1')
                                
                                recv_files[1] -= len(chunk)
                                
                            if recv_files[1] <= 0:
                                recv_files[0].close()
                                print('Arquivo Recebido!!!')
                                
                    else:
                        print('Recebendo arquivo em pedaços...\n')
                        
                        while True:
                            try:
                                c = int(data[pos:].decode())
                                pos += 1
                            except:
                                break;

                        # print('Data antes do Tam > {}'.format(data.decode()))
                        print('Pos. antes do Tam > {}'.format(pos))
                        tam = data[3:3+pos].decode()                                                                 
                        tam = int(tam)
                        print('Tamanho do Pedaço > {}\n'.format(tam))
                        pos = 3
                            
                        while len(data) >= tam:
                            if len(data[6:]) >= tam:
                                chunk = data[6:6+tam]
                                data = data[6+tam:]
                                #data_bytes = data_bytes[6+tam]
                                recv_files[0].write(chunk)
                            else:
                                falta = tam - len(data[6:])
                                resto = key.fileobj.recv(falta)
                                chunk = data[6:] + resto
                                recv_files[0].write(chunk)
                                data = ''
                                
                            recv_files[1] -= len(chunk)
                            
                        chunk = data[pos+3:] # aqui talvez tem um +3
                        recv_files[0].write(chunk)
                        recv_files[1] -= len(chunk)
                        
                        print('missing: {}'.format(recv_files[1]))
                        
                        if recv_files[1] <= 0:
                            recv_files[0].close()
                            print('Arquivo Recebido!')
                            
                # Se não for arquivo, ele mostra a resposta do cliente
                else:
                    if not data:
                        print('Cliente Desconectado > {}'.format(conn))
                        sel.unregister(conn)
                        conn.close()
                        continue
                    
                    print('\n'
                          'Cliente >>> {}\n'.format(data.decode()))
