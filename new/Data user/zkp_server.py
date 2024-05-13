import field
import Hash
import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from tinyec import registry
import json
from Crypto.Hash import SHA256
import random
#define
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)
#server parameter
pzs = 57
Pzs = pzs*curve.g
#zkp
idu = 123456
secret_number = 123

class Proof:
    def __init__(self, encrypted_random: field.Point, c: int, z: int, A: str):
        self.encrypted_random = encrypted_random
        self.c = c
        self.z = z
        self.A = A
    
    def display(self):
        print("Encrypted random: ")
        self.encrypted_random.display()
        print("c = ", self.c)
        print("z = ", self.z)

def zkp_generate(secret_info: int, ID: int, A: str):
    # random r and calc r*G
    r = random.randint(pow(2,254), pow(2,256))
    encrypted_r = r * curve.g

    # x*G
    public_info = secret_info * curve.g

    # challenge c = H(ID,g,g^r, g^x)
    c_bytes = Hash.hash_function(str(ID) + str(curve.g.x) + str(encrypted_r.x) + str(public_info.x))
    c_int = Hash.bytes_to_long(c_bytes)
    z = r + c_int * secret_info
    Proof(encrypted_r, c_int, z, A)

    return {'enc_r':encrypted_r.x,'c': c_int,'z':z,'A': A }

def encrypt_AES(key, plaintext):
    # Generate a random Initialization Vector (IV)
    iv = get_random_bytes(AES.block_size)
    
    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the plaintext
    padded_plaintext = pad(plaintext, AES.block_size)
    
    # Encrypt the plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # Return IV and ciphertext
    return iv, ciphertext
 

def decrypt_AES(key, iv, ciphertext):
    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt the ciphertext
    decrypted_plaintext = cipher.decrypt(ciphertext)
    
    # Unpad the decrypted plaintext
    unpadded_plaintext = unpad(decrypted_plaintext, AES.block_size)
    
    # Return the plaintext
    return unpadded_plaintext
def handle_client(conn, addr,server_pos):
    print(f"[NEW CONNECTION] {addr} connected.")
    client_pos = conn.recv(SIZE).decode(FORMAT)
    if client_pos == server_pos :
        conn.send("OK@Welcome to the Server.".encode(FORMAT))
    
        while True:
            data = conn.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            cmd = data[0]

            if cmd == "Data user Register":
                #recieve pack 1(R||)
                user_data = conn.recv(SIZE).decode(FORMAT)
                data = json.loads(user_data)
                R = data['R']
                iv = data['iv']
                ct = data['ct']
                k_new = SHA256.new(R*pzs)
                plaintext = decrypt_AES(k_new,iv,ct)
                plaintext = json.loads(plaintext)
                #validate Ai
                #if Ai valiated gen proof
                proof_dict = {}
                #proof_dict = {'A1' :{'enc_r':encrypted_r.x,'c': c_int,'z':z,'A': A1 }}
                for phyA, A in plaintext.items():
                    proof_dict[A] = zkp_generate(secret_number,idu,A)
                proof_dict_str = json.dumps(proof_dict)
                ct = encrypt_AES(k_new,proof_dict_str)#bytes
                conn.send(ct)#send E(proff||A)

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