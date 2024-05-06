from cp_abe import abe
from charm.toolbox.pairinggroup import PairingGroup, G1, G2, GT, extract_key
from AES_CBC import SymmetricEncryption
from PIL import Image
import sys
sys.path.insert(0, '/home/hung/project')
import time
import json
#path
key_path = '/home/hung/project/uc/uc_data/pkmk.txt'
text_path = '/home/hung/project/uc/uc_data/data.txt'
image_path ='/home/hung/project/uc/uc_data/pattern.png'
pdf_path = '/home/hung/project/uc/uc_data/donthuoc.pdf'
enc_data_path ='/home/hung/project/uc/uc_data/encrypted_data.txt'
pres_path = '/home/hung/project/uc/uc_data/encrypted_presciption.txt'
enc_key_path ='/home/hung/project/uc/uc_data/encrypted_key.txt'
enc_img_path = '/home/hung/project/uc/uc_data/encrypted_img.png'
group = PairingGroup('SS512')
cpabe = abe(group)
#Setup algorithm to generate public key PK and master key MK
(pk, mk) = cpabe.setup()
with open(key_path, 'w') as pkmk:
    pkmk.writelines([json.dumps(pk),'\n', json.dumps(mk)])

#print(pk, mk)
print('----SAVING PK, MK----')

print('----READING PK, MK----')

#Select subtree from tree to generate access policy
'''...'''

#access structure to encrypt message M
access_policy = '((a or b) and (c or d)) and (e or (f or (g and h)))'
#print("Attributes =>", attrs); print("Policy =>", access_policy)
#Encrypt message
'''
group = PairingGroup('SS512')
cpabe = abe(group)
msg = b'1234'
enc_key, cipher = cpabe.encrypt(pk, msg, access_policy)
print(enc_key, cipher)
'''

#Select data type for encryption 
choice = input("""Select data type for encryption:
1: encrypt text file               
2: encrypt pdf file                
3: encrypt image file (png):\n""")
if choice == '1':   #encrypt text file
    
    with open(text_path, 'rb') as input_data:
        msg = input_data.read()
elif choice == '2': #encrypt pdf file

    with open(pdf_path,'rb') as input_data:
        msg = input_data.read()
elif choice =='3':  #encrypt image file
    with open(image_path, 'rb') as input_data:
        msg = input_data.read()
else:
    print(False)
    sys.exit()
#if debug: print("msg =>", msg)
#print('----STARTING ENCRYPTION----')
group = PairingGroup('SS512')
cpabe = abe(group)
enc_key, cipher = cpabe.encrypt(pk, msg, access_policy)

print('----SUCCESSFULLY ENCRYPTED----')
#Write encrypted data to file
if choice == '1':   #encrypt text file
    with open(enc_data_path, 'w') as enc_data:
        enc_data.write(json.dumps(cipher))
    with open(enc_key_path, 'w') as key:
        key.write(json.dumps(enc_key))

elif choice == '2': #encrypt pdf file
    with open(pres_path,'w') as enc_pre:
        enc_pre.write(json.dumps(cipher))
    with open(enc_key_path, 'w') as key:
        key.write(json.dumps(enc_key))
elif choice =='3':  #encrypt image file
    with open(enc_img_path, 'wb') as enc_img:
        input_data.write(bytes.fromhex(cipher['CipherText']))
    with open(enc_key_path, 'w') as key:
        key.write(json.dumps(enc_key))
