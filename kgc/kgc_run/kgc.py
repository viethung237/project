from datetime import datetime
from charm.toolbox.pairinggroup import PairingGroup
import sys
import json

sys.path.insert(0, '/home/hung/project')
pairing_group = PairingGroup('SS512')
from cpabe_pack.cp_abe import abe
from client.client import run_client
def gen_time():
    current_time = datetime.now()
    timestamp = current_time.timestamp()
    return timestamp
def key_gb():
    groupObj = PairingGroup('SS512')
    key_gen  = abe(groupObj)
    key = key_gen.setup()
    return key
def int_to_bytes(num):
    # Xác định số lượng byte cần thiết để biểu diễn số nguyên
    byte_length = (num.bit_length() + 7) // 8
   
    # Chuyển số nguyên thành đối tượng byte
    byte_representation = num.to_bytes(byte_length, byteorder='big')
   
    return byte_representation
path_pk = '/home/hung/project/kgc/kgc_data/pk.txt'
path_mk ='/home/hung/project/kgc/kgc_data/mk.txt'
##test
time = gen_time()
pk,mk = key_gb()

for key, value in pk.items():
    pk[key] = int.from_bytes(pairing_group.serialize(value), byteorder='big')
 
pk_json = json.dumps(pk)

with open(path_pk, 'w') as filepk:
    # Write data to the file
    filepk.write(pk_json)
'''
with open(path_mk, 'w') as filemk:
    # Write data to the file
    filemk.write(json.dumps(mk))
'''   
    
#run_client('0')

    








