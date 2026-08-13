# ALUNO: João Vitor Garcia Aguiar Mintz; RA: 10440421
import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clientes_conectados = []
maior_lance = 0.0

def adicionar_cliente(conn):
    clientes_conectados.append({ 
        'CONN': conn, 
        'LANCE': 0.0
    })

def alterar_lance(conn, lance):
    for cliente in clientes_conectados:
        if cliente['CONN'] == conn:
            cliente['LANCE'] = lance

def broadcast(maior_atual):
    for cliente in clientes_conectados:
        cliente['CONN'].sendall(f"\nNOVO LANCE! Valor de {maior_atual} reais".encode())

def valor_abaixo(conn, maior_atual):
    conn.sendall(f"\nERRO: Valor abaixo do maior lance atual de {maior_atual} reais".encode())

def rodar_leilao(conn):
    global maior_lance # Função global para que possa ser alterada por todas as threads

    conn.sendall(f"BEM VINDO AO LEILÃO!\nItem atual: Geladeira 2 portas!\n".encode())
    
    while True:

        print(f"Maior lance atual de {maior_lance} reais.")

        dados = conn.recv(1024)

        if not dados:
            break

        lance = float(dados.decode())
        lance_aceito = False

        # REGIÃO CRÍTICA:
        if lance > maior_lance:
            maior_lance = lance
            print(f"Lance recebido: {lance} reais!") # Aviso ao servidor
            lance_aceito = True
            

        else:
            print(f"O lance de {conn} foi abaixo do maior atual!") # Aviso ao servidor
            valor_abaixo(conn, maior_lance) # Aviso apenas ao cliente que enviou o valor abaixo

        # FINAL DA REGIÃO CRÍTICA
        if lance_aceito:
            broadcast(maior_lance) # Aviso a todos os clientes
            alterar_lance(conn, lance)


    conn.close()


def main():
    # INICIA O SOCKET
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))

    s.listen(5)

    while True:
        conn, addr = s.accept()

        # Cria thread para o cliente que acabou de entrar:
        adicionar_cliente(conn)
        print(f"Cliente conectado: {addr}")

        # Configura para paralelizar o servidor para aceitar mais de um cliente
        t = threading.Thread(target=rodar_leilao, args=(conn,))
        t.daemon = True
        t.start()   
        
        print(f"Leilão em Tempo Real ouvindo em {PORT}...")
        print("Aviso: Permitido múltiplos usuários simultâneos")

if __name__ == "__main__":
    main()