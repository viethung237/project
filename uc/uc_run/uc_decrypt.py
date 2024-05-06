from cp_abe import abe
from charm.toolbox.pairinggroup import PairingGroup, G1, G2, GT, extract_key
from AES_CBC import SymmetricEncryption
from PIL import Image
import sys
sys.path.insert(0, '/home/hung/project')
import time
import json
#path
enc_data_path ='/home/hung/project/uc/uc_data/encrypted_data.txt'
key_path = '/home/hung/project/uc/uc_data/pkmk.txt'
enc_key_path ='/home/hung/project/uc/uc_data/encrypted_key.txt'
print('----READING PK, MK----')
with open(key_path, 'r') as pkmk:
    lists = pkmk.readlines()
    pk, mk = json.loads(lists[0]), json.loads(lists[1])

group = PairingGroup('SS512')
cpabe = abe(group)
#print(pk, mk)
def get_pw():
    count = input('Number of attributes:')
    attrs = []
    for i in range(int(count)):
        attrs.append(input('Enter your attributes: ').upper())
    return attrs
#User enter attributes
attrs = get_pw()

#print(attrs)
#Generate secret key for decryption
secret_key = cpabe.keygen(pk, mk, attrs)
#print(secret_key)
#Load cipher and ct_key to decrypt
with open(key_path, 'r') as pkmk:
    lists = pkmk.readlines()
    pk, mk = json.loads(lists[0]), json.loads(lists[1])
with open(enc_key_path, 'r') as key:
    enc_key = json.loads(key.readline())
with open(enc_data_path, 'r') as data:
    cipher = json.loads(data.readline())    
#print(enc_key)
msg = cpabe.decrypt(pk, secret_key, enc_key, cipher)
print(msg)
