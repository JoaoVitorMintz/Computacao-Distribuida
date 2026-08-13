# ALUNO: João Vitor Garcia Aguiar Mintz; RA: 10440421
import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 5000))

    # Recebe mensagem inicial
    data = s.recv(4096).decode()

    if not data:
        print("ERRO: Mensagem inicial não recebida!")
        s.close()
        return

    print(data, end="")

    while True:
        resposta = input("Digite seu lance: ")
        s.sendall((resposta + "\n").encode())

        data = s.recv(4096).decode()
        if not data:
            break

        print(data, end="")
        
    s.close()


if __name__ == "__main__":
    main()