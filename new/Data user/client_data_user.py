import socket
import random
import hashlib
from Crypto.Hash import SHA256
import field
from tinyec import registry
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import json

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


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




r = random.randint(pow(2,254), pow(2,256))
R = r*curve.g
#zkp check
pzs = 57
Pzs = pzs*curve.g
#user
k = SHA256.new(int_to_bytes(r*Pzs.x)).digest()
data = {'phyA1':'A1', 'phyA2':'A2'}
#encrypt
data = json.dumps(data)
iv,ciphertext = encrypt_AES(k,data.encode(FORMAT))
print(decrypt_AES(k,iv,ciphertext))
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

        if cmd == "Data user Register":
            client.send(cmd.encode(FORMAT))
            send_data = {'R': R.x ,'iv': iv, 'ct': ciphertext}
            client.send(json.dumps(send_data).encode(FORMAT))#send(R||ct)
            pack_2 = client.recv(SIZE)#recieve pack 2(proof||A)
            data = decrypt_AES(k,iv,pack_2) #{'A1' :{'enc_r':encrypted_r.x,'c': c_int,'z':z,'A': A1 }}
            data = json.loads(data)
            #unpack, store proof
        
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
    print("Disconnected from the server.")
    client.close()
