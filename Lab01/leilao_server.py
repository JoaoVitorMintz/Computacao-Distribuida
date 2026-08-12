# ALUNO: João Vitor Garcia Aguiar Mintz; RA: 10440421
import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

def fundo(preco, provento):
    return {
        'PRECO': preco,
        'PROVENTO': provento,
        'STATUS': preco + provento
    }

# Com base no dia 08/12/2026
FUNDOS = {
    'BRCO11': fundo(114.12, 1.05),
    'BTLG11': fundo(99.88, 0.81),
    'HGLG11': fundo(147.76, 1.10),
    'KNRI11': fundo(154.95, 1.38),
    'MXRF11': fundo(9.60, 0.10),
    'PVBI11': fundo(70.49, 0.40),
    'XPCI11': fundo(83.69, 0.95),
    'MCCI11': fundo(95.10, 1.00),
    'KNCR11': fundo(106.50, 1.10),
    'VISC11': fundo(105.42, 0.84)
}

def comandos(conn):
    # Este b já torna em bytes, não precisa do encode no final
    conn.sendall(b"\n--- CONSULTA FINANCEIRA (MODO SEQUENCIAL) ---\n\n")
    conn.sendall(b"Comandos: PRECO;TICKER | PROVENTO;TICKER | STATUS;TICKER\n")
    conn.sendall(b"Digite SAIR para encerrar.\n\n")

    conn.sendall(b"> ")
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        comando = data

        if comando == 'SAIR':
            conn.sendall(b"\nPROCESSO FINALIZADO!\n")
            break

        partes = comando.split(";")

        if len(partes) != 2:
            conn.sendall(b"\nERRO: Formato invalido. Use COMANDO;TICKER ou SAIR\n")
            conn.sendall(b"> ")
            continue

        cmd, ticker = partes[0], partes[1]

        if ticker not in FUNDOS.keys():
            conn.sendall(b"\nERRO: FII nao encontrado\n")
            conn.sendall(b"> ")
            continue

        if cmd not in FUNDOS[ticker].keys():
            conn.sendall(b"\nERRO: Comando invalido\n")
            conn.sendall(b"> ")
            continue

        valor = FUNDOS[ticker][cmd]
        conn.sendall(f"{valor}\n".encode())
        conn.sendall(b"> ")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    conn, addr = s.accept()
    t = threading.Thread(target=comandos, args=conn)
    t.start()
    t.daemon = True
    
    print(f"Leilão em Tempo Real ouvindo em {PORT}...")
    print("Aviso: Permitido múltiplos usuários simultâneos")

    while True:
        conn, addr = s.accept()
        print(f"Atendendo agora: {addr}")
        
        comandos(conn) # O código "trava" aqui até a função terminar
        
        conn.close()
        print(f"Cliente {addr} finalizado. Pronto para o próximo.\n")

if __name__ == "__main__":
    main()