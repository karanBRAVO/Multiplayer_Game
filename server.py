import socket
from _thread import *
import colorama
from colorama import Fore, Back, Style

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
colorama.init(autoreset=True)

IP = socket.gethostbyname(socket.gethostname())
PORT = 5689
ADDR = (IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "...left"
REFUSED_MESSAGE = "[REFUSED] server refused to join"
CONN_LIST = []
OBJ_LIST = []
USER_CONNECT_COUNT = 0

SOCKET.bind(ADDR)


def handleClientData(conn, addr, conn_list):
    global USER_CONNECT_COUNT
    print(Fore.BLACK + Back.MAGENTA + f"[NEW CLIENT] {addr[0]} : {addr[1]}")
    USER_CONNECT_COUNT += 1

    while True:
        try:
            CLIENT_DATA = conn.recv(1024)
            if CLIENT_DATA:
                CLIENT_MESSAGE = CLIENT_DATA.decode(FORMAT)
                print(Fore.GREEN + f"[RECEIVED] {addr[1]}: {CLIENT_MESSAGE}")
                if CLIENT_MESSAGE != "--user joined" and CLIENT_MESSAGE != DISCONNECT_MESSAGE and USER_CONNECT_COUNT < 3:
                    TUP = (conn, CLIENT_MESSAGE)
                    OBJ_LIST.append(TUP)
                    if len(OBJ_LIST) >= 2:
                        if OBJ_LIST[len(OBJ_LIST) - 2][0] != OBJ_LIST[len(OBJ_LIST) - 1][0]:
                            MSG = "--user joined"
                            OBJ_LIST[len(OBJ_LIST) - 1][0].send(MSG.encode(FORMAT))
                            MSG = OBJ_LIST[len(OBJ_LIST) - 2][1]
                            OBJ_LIST[len(OBJ_LIST) - 1][0].send(MSG.encode(FORMAT))
                if USER_CONNECT_COUNT > 2 and CLIENT_MESSAGE != DISCONNECT_MESSAGE and CLIENT_MESSAGE != REFUSED_MESSAGE:
                    MSG = "[SERVER] two users have already joined"
                    conn_list[len(conn_list) - 1].send(MSG.encode(FORMAT))
                if len(conn_list) > 1:
                    for i in range(0, len(conn_list)):
                        if conn_list[i] != conn:
                            print(Fore.BLACK + Back.BLUE + "[SENDING] sending messages ...")
                            if CLIENT_MESSAGE == DISCONNECT_MESSAGE:
                                MSG = "--user left"
                            elif CLIENT_MESSAGE == REFUSED_MESSAGE:
                                MSG = "--user refused by server"
                            else:
                                MSG = CLIENT_MESSAGE
                            SEND_MESSAGE = MSG.encode(FORMAT)
                            conn_list[i].send(SEND_MESSAGE)
                            print(Fore.BLACK + Back.GREEN + "--[SUCCESS] message sent successfully ...")
                if CLIENT_MESSAGE == DISCONNECT_MESSAGE or CLIENT_MESSAGE == REFUSED_MESSAGE:
                    MSG = "[SERVER]: Bye"
                    conn.send(MSG.encode(FORMAT))
                    conn_list.pop(conn_list.index(conn))
                    USER_CONNECT_COUNT -= 1
                    break
        except ConnectionResetError as err:
            print(err)

    print(Fore.MAGENTA + "[CLOSING] closing the connection ...")
    conn.close()
    print(Fore.BLACK + Back.CYAN + f"--closed for {addr[1]}")


def startServer():
    SOCKET.listen(0)
    print(Fore.YELLOW + Style.BRIGHT + f"[LISTENING] (on port {PORT}) server is listening  ...")

    while True:
        print(Fore.BLUE + "[WAITING] waiting for connections ...")
        conn, addr = SOCKET.accept()
        CONN_LIST.append(conn)
        start_new_thread(handleClientData, (conn, addr, CONN_LIST))


if __name__ == "__main__":
    print(Fore.YELLOW + Style.BRIGHT + "[STARTING] server is starting ...")
    startServer()
