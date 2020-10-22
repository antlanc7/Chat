import socket,time,sys,datetime
from _thread import *

server = ""
port = 3125
addr = (server,port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(10)
print("Server avviato sulla porta",port)

clients = []

def threaded_client(conn, addr):
    print('Il client ', addr, ' si è connesso')
    nickname = conn.recv(256).decode("utf-8")
    welcome_message="Benvenuto "+nickname
    print(welcome_message)
    for (other_conn, _) in clients:
        other_conn.send(welcome_message.encode())
    while True:
        try:
            data = conn.recv(256).decode("utf-8")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = "[" + timestamp + "]" + nickname + " : " + data
            print(message)
            for (other_conn,_) in clients:
                if conn!=other_conn:
                    other_conn.send(message.encode())
            time.sleep(0.1)
        except:
            break

    print("Il client", addr, nickname, "si è disconnesso")
    conn.close()
    clients.remove((conn,addr))


while True:
    conn, addr = s.accept()
    clients.append((conn, addr))
    start_new_thread(threaded_client, (conn, addr))


