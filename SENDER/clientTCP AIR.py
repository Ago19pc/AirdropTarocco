import os.path
from socket import *


serverName = input("IP RICEVENTE: ")
serverPort = 12001

if __name__ == "__main__":

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.settimeout(10)

    try:
        clientSocket.connect((serverName, serverPort))
        while 1:
            filename = input("NOMEFILE: ")

            if filename == '.':
                break

            file = open(filename, "rb")

            file_size = os.path.getsize(filename)

            clientSocket.sendall(filename.encode('utf-8'))
            clientSocket.sendall(b"<NAME-END>")

            # WAIT FOR RECEIVE
            while True:
                okMessage = clientSocket.recv(1024).decode('utf-8')
                if okMessage == f"OK CONTINUE":
                    break

            okMessage = f""
            clientSocket.sendall(str(file_size).encode('utf-8'))
            clientSocket.sendall(b"<SIZE-END>")

            # WAIT FOR RECEIVE
            while True:
                okMessage = clientSocket.recv(1024).decode('utf-8')
                if okMessage == f"OK CONTINUE":
                    break

            while True:
                data = file.read(1024)
                print("FILE READ")
                if data == '':
                    break
                clientSocket.sendall(data)
            clientSocket.sendall(b"<END>")

            print(f"FILE {filename} INVIATO")

            file.close()

            modifiedMessage = clientSocket.recv(1024)
            print(f"Dal server: {modifiedMessage.decode('utf-8')}")

        clientSocket.close()

    except timeout:
        print("Timeout scaduto")
    finally:
        clientSocket.close()



