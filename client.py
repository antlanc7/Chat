import socket, select
from _thread import start_new_thread
s = socket.socket()

ip="localhost"
port = 3125
s.connect((ip, port))
username = input("Inserisci l'username con il quale verrai identificato: ")
if (s.recv(1024).decode()=="NAME"):
    s.sendall(username.encode())

def print_received_messages(s):
    while s:
        ready = select.select([s], [], [], 1)
        if ready[0]:
            try:
                print(s.recv(400).decode())
            except:
                return

start_new_thread(print_received_messages,(s,))

while True:
    z = input()
    ready = select.select([], [s], [], 1)
    if ready[1]:
        try:
            s.sendall(z.encode())
        except:
            break
