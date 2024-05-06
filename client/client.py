
#for socket
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
        elif cmd == "OK" and msg == '[NOT POS]':
            print(f"{msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")
        

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))
        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        elif cmd == "UPLOAD":
            path = data[1]
        

            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))
        elif cmd == "REQUEST":
            path = data[1]

            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))
           

        elif cmd == "DOWNLOAD":
            send_data = f"{cmd}@{data[1]}"
            client.send(send_data.encode(FORMAT))
            data = client.recv(SIZE).decode(FORMAT)
            data = data.split("@")

            print('data sau:',data)
            
            
            CLIENT_DATA_PATH = '/home/hung/test/client/client_data'
            name, text = data[1], data[2]
            filepath = os.path.join(CLIENT_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)

            send_data = "OK@File downloaded successfully."
            client.send(send_data.encode(FORMAT))
            
    print("Disconnected from the server.")
    client.close()

#run_client('0')