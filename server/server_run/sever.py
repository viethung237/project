
import os
import socket
import threading
#one server test
import sys
sys.path.insert(0, '/home/hung/project')
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from zkp import zkp_generate,zkp_verify,Proof
group = PairingGroup('SS512')
#multi test   



IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = '/home/hung/project/Fog/fog_data/'

def handle_client(conn, addr,server_pos):
    print(f"[NEW CONNECTION] {addr} connected.")
    client_pos = conn.recv(SIZE).decode(FORMAT)
    if client_pos == server_pos :
        conn.send("OK@Welcome to the Server.".encode(FORMAT))
    
    


        while True:
            data = conn.recv(SIZE).decode(FORMAT)
            print('data1:',data)
            data = data.split("@")
            print('data2:',data)
            cmd = data[0]

            if cmd == "LIST":
                files = os.listdir(SERVER_DATA_PATH)
                send_data = "OK@"

                if len(files) == 0:
                    send_data += "The server directory is empty"
                else:
                    send_data += "\n".join(f for f in files)
                conn.send(send_data.encode(FORMAT))

            elif cmd == "UPLOAD":
                name, text = data[1], data[2]
                print('name:',name)
                print('text:',text)
                filepath = os.path.join(SERVER_DATA_PATH, name)
                print('filepath : ',filepath)
                with open(filepath, "w") as f:
                    f.write(text)

                send_data = "OK@File uploaded successfully."
                conn.send(send_data.encode(FORMAT))
            elif cmd == "DOWNLOAD":
                path = data[1]

                with open(f"{path}", "r") as f:
                    text = f.read()

                filename = path.split("/")[-1]
                send_data = f"{cmd}@{filename}@{text}"
                conn.send(send_data.encode(FORMAT))


            elif cmd == "DELETE":
                files = os.listdir(SERVER_DATA_PATH)
                send_data = "OK@"
                filename = data[1]

                if len(files) == 0:
                    send_data += "The server directory is empty"
                else:
                    if filename in files:
                        os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                        send_data += "File deleted successfully."
                    else:
                        send_data += "File not found."

                conn.send(send_data.encode(FORMAT))
            elif cmd == 'REQUEST':
                name, text = data[1], data[2]
                filepath = os.path.join(SERVER_DATA_PATH, name)
                with open(filepath, "w") as f:
                    f.write(text)
                with open(filepath, 'r') as readata:
                    list = []
                    for line in readata:
                        list.append(line.strip())
                    e  = group.deserialize(list[0].encode('utf-8'))
                    c = int(list[1])
                    z = int(list[2])
                    public_info = group.deserialize(list[3].encode('utf-8'))
                    g = group.deserialize(list[4].encode('utf-8'))
                    zkproof_real = Proof(e, c, z)
                    verify = zkp_verify(zkproof_real, public_info,1,g)
                if verify == 1:
                    send_data = "OK@True"
                    conn.send(send_data.encode(FORMAT))
                if verify == 0:
                    send_data = "OK@False"
                    conn.send(send_data.encode(FORMAT))
                    conn.close()
                    
    
            elif cmd == "LOGOUT":
                break
            elif cmd == "HELP":
                data = "OK@"
                data += "LIST: List all the files from the server.\n"
                data += "UPLOAD <path>: Upload a file to the server.\n"
                data += "DELETE <filename>: Delete a file from the server.\n"
                data += "LOGOUT: Disconnect from the server.\n"
                data += "HELP: List all the commands."
                data += "DOWNLOAD: Get file from server"

                conn.send(data.encode(FORMAT))

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
'''
#runserver('0')
with open('/home/hung/project/Fog/fog_data/uc_zkp_data.txt', 'r') as readata:
    list = []
    for line in readata:
        list.append(line.strip())
    e  = group.deserialize(list[0].encode('utf-8'))
    c = int(list[1])
    z = int(list[2])
    public_info = group.deserialize(list[3].encode('utf-8'))
    g = group.deserialize(list[4].encode('utf-8'))
    zkproof_real = Proof(e, c, z)
    #print(zkproof_real)
    verify = zkp_verify(zkproof_real, public_info,1,g) 
    print(verify)
'''