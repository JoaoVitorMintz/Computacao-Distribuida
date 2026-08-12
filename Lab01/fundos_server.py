import socket

HOST = "0.0.0.0"
PORT = 5000

def fundo(preco, provento):
    return {
        'PRECO': preco,
        'PROVENTO': provento,
        'STATUS': preco + provento
    }

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

def jogar(conn):
    conn.sendall("\n--- CONSULTA FINANCEIRA (MODO SEQUENCIAL) ---\n\n".encode())
    comando = input(conn.sendall(">"))
    while(comando != 'SAIR'):
        resul_comando = comando.split(':')
        if (resul_comando not in FUNDOS.keys):
            conn.sendall("\nERRO: FII não encontrado")
        else:
            
    
    
            
    conn.sendall(f"PROCESSO FINALIZADO!".encode())

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1) # Fila pequena para demonstrar o limite
    
    print(f"Consultas Financeiras (Sem Threads) ouvindo em {PORT}...")
    print("Aviso: Apenas um cliente por vez será atendido.")

    while True:
        conn, addr = s.accept()
        print(f"Atendendo agora: {addr}")
        
        jogar(conn) # O código "trava" aqui até a função terminar
        
        conn.close()
        print(f"Cliente {addr} finalizado. Pronto para o próximo.\n")

if __name__ == "__main__":
    main()