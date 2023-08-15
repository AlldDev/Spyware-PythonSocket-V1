################################################################################
# Imports
################################################################################
import socket
import selectors
import types

################################################################################
# Constants, definitions and global variables
################################################################################
_HOST = '127.0.0.1'
_PORT = 9999

_MAX_MSG_SIZE = 4096

################################################################################
# Functions and procedures
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Main
################################################################################
if __name__ == "__main__":
    sel = None     # Selector
    sock = None    # Socket para escutar novas conexões
    events = None  # Eventos encontrados pelo selector
    conn = None    # Conexão
    addr = None    # Endereço
    key = None     # Auxiliar para trabalhar com os eventos
    mask = None    # Auxiliar para trabalhar com os eventos

    # Inicializando nosso 'DefaultSelector'
    sel = selectors.DefaultSelector()

    # Criando o socket
    # AF_INET : formato (host, port)
    # SOCK_STREAM : TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Faz a ligação do socket com o endereço
    sock.bind((_HOST, _PORT))

    # Começa a escutar por conexões, o argumento 100 é opcional e
    # indica quantas conexões podem ficar 'na espera' para serem
    # aceitas antes do servidor começar a recusar conexões
    sock.listen(100)

    # Configurando nosso socket como não bloqueante
    sock.setblocking(False)

    # Registrando nosso socket com o selector
    sel.register(sock, selectors.EVENT_READ)

    ########################################
    # Loop principal
    ########################################
    while True:
        events = sel.select()

        for key, mask in events:

            # Recebendo algo no socket para novas conexões
            if key.fileobj == sock:
                # Aceitando a nova conexão
                conn, addr = sock.accept()

                # Configurando a nova conexão como não bloqueante
                conn.setblocking(False)

                # Registrando a nova conexão com o selector
                sel.register(conn, selectors.EVENT_READ)

                print("Nova conexão {}".format(key.fileobj))

            # Recebendo em outros sockets
            else:
                # Se é um evento de leitura
                if mask & selectors.EVENT_READ:
                    # Recebendo a mensagem
                    data = key.fileobj.recv(_MAX_MSG_SIZE)

                    # Convertendo de bytes para string
                    data = bytes.decode(data, 'utf-8')

                    # Se não recebemos nada, o cliente quer fechar a conexão
                    if not data:
                        print("Fechando conexão {}".format(key.fileobj))
                        sel.unregister(key.fileobj)
                        key.fileobj.close()
                        continue

                    # Se o cliente não fechou a conexão, podemos tratar a mensagem
                    print("[{}] {}".format(key.fileobj, data))