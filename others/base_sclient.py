################################################################################
# Imports
################################################################################
import socket
import selectors
import sys

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
    sel = None  # Selector
    sock = None  # Socket para conexão
    key = None  # Auxiliar para trabalhar com os eventos
    mask = None  # Auxiliar para trabalhar com os eventos
    events = None  # Eventos recebidos do selector
    data = None
    # Inicializando nosso 'DefaultSelector'
    sel = selectors.DefaultSelector()

    # Criando o socket
    # AF_INET : formato (host, port)
    # SOCK_STREAM : TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurando como não bloqueante
    sock.setblocking(False)

    # Conectando
    sock.connect_ex((_HOST, _PORT))

    # Regsitrando nosso socket com o selector
    sel.register(sock, selectors.EVENT_READ)

    # Registrando o 'stdin' (usuário digitando) com o selector
    sel.register(sys.stdin.fileno(), selectors.EVENT_READ)

    ########################################
    # Loop principal
    ########################################
    while True:
        events = sel.select()

        for key, mask in events:
            # O usuário digitou algo
            if key.fileobj == sys.stdin.fileno():
                # Lendo a mensagem da entrada padrão
                data = sys.stdin.readline()

                # /msg Texto
                if data[0:4] == '/msg':
                    sock.sendall((bytes("msg{}".format(data[5:])))

                elif data[0:4] == '/cmd':
                    # ncurses -> lib
                    # Enviando para o servidor
                    # Com a conversão de string para bytes
                    sock.sendall(bytes(data, 'utf-8'))
                    # Recebemos algo em outro socket
                else:
                    # Recebendo os dados do socket
                    data = key.fileobj.recv(_MAX_MSG_SIZE)

                    if not data:
                        exit()

                    # Convertendo de bytes para string
                    data = bytes.decode(data, 'utf-8')

                    print("[{}] {}".format(key.fileobj, data))
