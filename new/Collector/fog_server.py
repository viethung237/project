import os
import socket
import threading
#define
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def handle_client(conn, addr,server_pos):
    print(f"[NEW CONNECTION] {addr} connected.")
    client_pos = conn.recv(SIZE).decode(FORMAT)
    if client_pos == server_pos :
        conn.send("OK@Welcome to the Server.".encode(FORMAT))
    
    


        while True:
            data = conn.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            cmd = data[0]

            if cmd == "Collector Register":
                #recieve Di 
                client_data = conn.recv(SIZE).decode(FORMAT)
                #store Di,MAC
                #send A
                
                if 1 :
                    conn.send('serverdata'.encode(FORMAT))
                else :
                    conn.send('INVALID'.encode(FORMAT))
                    break

            elif cmd == "LOGOUT":
                break
    
        print(f"[DISCONNECTED] {addr} disconnected")
        conn.close()
    else:
        conn.send("OK@[NOT POS]".encode(FORMAT))
        conn.close()

def runserver(server_pos):
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr,server_pos))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")