# ALUNO: João Vitor Garcia Aguiar Mintz; RA: 10440421
import socket
import threading

def receber_mensagem(s):
    while True:
        data = s.recv(4096)

        if not data:
            break

        print("\n" + data.decode().strip())
        print("Digite seu lance: ", end="", flush=True)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 5000))

    # Recebe a primeira mensagem inicial antes de criar a thread:
    data = s.recv(4096).decode()
    print(data, end="")

    t = threading.Thread(target=receber_mensagem, args=(s,))
    t.daemon = True
    t.start()

    try:
        while True:
            resposta = input("Digite seu lance: ")

            if not resposta.strip():
                continue

            s.sendall((resposta + "\n").encode())

    except KeyboardInterrupt:
        print("\nCliente encerrado.")

    finally:
        s.close()

if __name__ == "__main__":
    main()