# ALUNO: João Vitor Garcia Aguiar Mintz; RA: 10440421
import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

MAX_CLIENTS = 5

clientes_conectados = []
maior_lance = 0.0

def adicionar_cliente(conn, id):
    clientes_conectados.append({ 
        'CONN': conn,
        'ID': id,
        'LANCE': 0.0
    })

def alterar_lance(conn, lance):
    for cliente in clientes_conectados:
        if cliente['CONN'] == conn:
            cliente['LANCE'] = lance

def broadcast(id, maior_atual):
    for cliente in clientes_conectados:
        cliente['CONN'].sendall(f"\nNovo lance, R${maior_atual} por {id}".encode())

def valor_abaixo(conn):
    conn.sendall(f"\nLANCE RECUSADO: Valor baixo".encode())

def rodar_leilao(conn, id):
    global maior_lance

    conn.sendall(
        f"BEM VINDO AO LEILÃO!\n"
        f"Você é o Cliente {id}\n"
        f"Item atual: Geladeira 2 portas!\n".encode()
    )

    while True:

        print(f"Maior lance atual de {maior_lance} reais.")

        dados = conn.recv(1024)

        if not dados:
            break

        lance_texto = dados.decode().strip()

        if not lance_texto:
            continue

        lance = float(lance_texto)

        lance_aceito = False

        # REGIÃO CRÍTICA
        if lance > maior_lance:
            maior_lance = lance

            print(f"Lance recebido: {lance} reais!")
            lance_aceito = True

        else:
            print(f"O lance do Cliente {id} foi abaixo do maior atual!")
            valor_abaixo(conn)

        # FINAL DA REGIÃO CRÍTICA
        if lance_aceito:
            alterar_lance(conn, lance)
            broadcast(id, maior_lance)

    for cliente in clientes_conectados:
        if cliente['CONN'] == conn:
            clientes_conectados.remove(cliente)
            break

    conn.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    num_cliente = 0  

    while True:
        conn, addr = s.accept()

        if len(clientes_conectados) >= MAX_CLIENTS:
                conn.sendall("Servidor cheio! Máximo de 5 clientes.\n".encode())
                conn.close()
                continue

        adicionar_cliente(conn, num_cliente)
        print(f"Cliente {num_cliente} conectado: {addr}")

        t = threading.Thread(target=rodar_leilao, args=(conn, num_cliente))
        t.daemon = True
        t.start()

        num_cliente += 1

if __name__ == "__main__":
    main()