import socket
import os
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def run_client(pos):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(pos.encode(FORMAT))
    
    

    while True:
        
        data = client.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        print('client data:',data)
        cmd =data[0]
        msg = data[1]
        

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")
        

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "Register":
            client.send(cmd.encode(FORMAT))
            send_data = 'client_data'
            client.send(send_data.encode(FORMAT))
            client.recv(SIZE).decode(FORMAT)
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
    print("Disconnected from the server.")
    client.close()

    