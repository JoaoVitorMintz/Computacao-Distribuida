import socket
import threading

HOST = "localhost"
PORT = 5000

NUM_CLIENTES = 5       # Quantidade de clientes simulados
REQUISICOES_POR_CLIENTE = 50  # Quantidade de incrementos por cliente

def cliente_simulado():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        for _ in range(REQUISICOES_POR_CLIENTE):
            client.send("COMPRAR".encode())
            resposta = client.recv(1024).decode()
            print(resposta)
            if "Estoque restante: 0" in resposta:
                client.close()
                return
            if "Produto esgotado" in resposta:
                client.close()
                return

        client.close()

    except:
        pass

threads = []
print("Iniciando teste de estresse...")
for _ in range(NUM_CLIENTES):
    t = threading.Thread(target=cliente_simulado)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Teste finalizado.")
