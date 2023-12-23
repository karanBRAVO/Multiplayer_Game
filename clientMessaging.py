import socket

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = socket.gethostbyname(socket.gethostname())
PORT = 5689
ADDR = (IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "...left"


def connectTOserver(address):
    try:
        CLIENT_SOCKET.connect(address)
        print("[CONNECTED] connected to server :)")
    except socket.error:
        print("[!NOT FOUND] cannot connect :(")

    while True:
        MESSAGE = input(">> ")
        DATA = MESSAGE.encode(FORMAT)
        CLIENT_SOCKET.send(DATA)
        if MESSAGE == DISCONNECT_MESSAGE:
            break

    print("[CLOSING] closing socket ...")
    CLIENT_SOCKET.close()
    print("--closed")


if __name__ == "__main__":
    print("[CONNECTING] trying to connect ...")
    connectTOserver(ADDR)
