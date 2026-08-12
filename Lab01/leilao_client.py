# ALUNO: João Vitor Garcia Aguiar Mintz; RA: 10440421
import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 5000))

    while True:
        data = s.recv(4096).decode()
        if not data:
            break

        if data.endswith("> "):
            resposta = input(data)
            s.sendall((resposta + "\n").encode())
        else:
            print(data, end="")

    s.close()


if __name__ == "__main__":
    main()