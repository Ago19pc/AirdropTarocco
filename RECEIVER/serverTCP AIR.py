from socket import *
from threading import Thread
import tqdm


def handler(connectionSocket):
    while 1:

        file_name = b""

        while True:
            name_data = connectionSocket.recv(1024)
            file_name += name_data
            if file_name[-10:] == b"<NAME-END>":
                break

        # SEND OK CONTINUE
        connectionSocket.sendall(f"OK CONTINUE".encode('utf-8'))

        file_name = file_name[:-10].decode('utf-8')

        if file_name == '.':
            break

        print(f"FILE NAME: {file_name}")

        file_size = b""
        while True:
            size_data = connectionSocket.recv(1024)
            file_size += size_data
            if file_size[-10:] == b"<SIZE-END>":
                break

        # SEND OK CONTINUE
        connectionSocket.sendall(f"OK CONTINUE".encode('utf-8'))

        file_size = int(file_size[:-10])
        print(f"FILE SIZE: {file_size}")

        file = open(file_name, "wb")

        file.close()
        file = open(file_name, "ab")

        file_bytes = b""

        progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))

        while True:
            data = connectionSocket.recv(1024)
            # file_bytes += data
            progress.update(len(data))
            if file_bytes[-5:] == b"<END>":
                file.write(data[:-5])
                break
            file.write(data)

        file.close()
        connectionSocket.sendall(f"FILE {file_name} RICEVUTO".encode('utf-8'))
        print(f"FILE {file_name} RICEVUTO")
        #file_bytes = file_bytes[:-5]
        #file.write(file_bytes)
        #file.close()

    connectionSocket.close()
    print("CONNESSIONE TERMINATA")


serverPort = 12001

if __name__ == "__main__":
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("Il server è pronto a ricevere")

    while 1:
        connectionSocket, clientAddress = serverSocket.accept()
        print(f"Connesso con: {clientAddress}")
        thread = Thread(target=handler, args=(connectionSocket,))
        thread.start()
