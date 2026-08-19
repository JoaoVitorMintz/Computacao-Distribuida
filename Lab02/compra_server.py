import socket
import threading

HOST = "0.0.0.0"
PORT = 5000
lock = threading.Lock()

estoque = 10 # Variável inicializada em 10

clientes_conectados = []

def adicionar_cliente(conn, id):
    clientes_conectados.append({ 
        'CONN': conn,
        'ID': id
    })

def broadcast():
    for cliente in clientes_conectados:
        cliente['CONN'].sendall(f"\nEstoque finalizado! Sem mais produtos...".encode())

def realizar_compra(conn, id):
    global estoque

    conn.sendall("Compra online, escreva 'COMPRAR' ou 'CONSULTAR' e 'sair' para fechar\n".encode())

    while True:
        if estoque == 0:
            broadcast()

        print(f"Quantidades de produtos atualmente: {estoque}")

        dados = conn.recv(1024).decode().strip().upper()

        if not dados:
            break

        comando = dados

        if comando == "COMPRAR":
            with lock:
                if estoque > 0: 
                    estoque -= 1
                    conn.sendall(f"Compra realizada. Estoque restante: {estoque}.".encode())
                    print(f"Compra de {id}.")
                elif estoque == 0: 
                    conn.sendall("ERRO: Produto esgotado.".encode())
                    print(f"Erro na compra de {id}.")
                else:
                    conn.sendall("Valor invalido.".encode())
                    print(f"Tentativa de compra inválida de {id}.")
        elif comando == "CONSULTAR":
            conn.sendall(f"Estoque atual: {estoque}".encode())
            print(f"Consulta de Estoque de {id}.")

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


        adicionar_cliente(conn, num_cliente)
        print(f"Cliente {num_cliente} conectado: {addr}")

        t = threading.Thread(target=realizar_compra, args=(conn, num_cliente))
        t.daemon = True
        t.start()

        num_cliente += 1

if __name__ == "__main__":
    main()