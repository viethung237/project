import socket
import os
from Crypto.Hash import SHA256
from getmac import get_mac_address as gma
import field
from tinyec import registry

MAC = gma()
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
ID = 123456

samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)


def int_to_bytes(number):
    byte_length = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_length, byteorder='big')
def bytes_to_int(number):
    integer_value = int.from_bytes(number, byteorder='big')  
    return integer_value

def get_mac_client(MAC):
    mac =''
    for i in MAC:
        if i != ':':
            mac += i
    mac = int(mac,16) 
    return int_to_bytes(mac)

def get_di(id,mac):
    id  = int_to_bytes(id)
    return SHA256.new(id+mac).digest()
def get_Di(di):
    di = bytes_to_int(di)
    return di*curve.g

mac = get_mac_client(MAC)
di = get_di(ID,mac)
Di = get_Di(di)


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

        if cmd == "Collector Register":
            client.send(cmd.encode(FORMAT))
            send_data = Di.x+Di.y
            client.send(send_data.encode(FORMAT))
            client.recv(SIZE).decode(FORMAT)
        
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
    print("Disconnected from the server.")
    client.close()
