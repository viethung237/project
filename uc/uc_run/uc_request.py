import sys
sys.path.insert(0, '/home/hung/project')
uc_data_path = '/home/hung/project/uc/uc_data/uc_zkp_data.txt'
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from zkp import zkp_generate,zkp_verify,Proof
from client.client import run_client

group = PairingGroup('SS512')
real_info = 345
fake_info = 344
e, c, z, g = zkp_generate(real_info,1)
public_info = g ** real_info
zkproof_real = Proof(e, c, z)


with open(uc_data_path, 'w') as data:
    e_decode = group.serialize(e).decode('utf-8')
    public_info = group.serialize(public_info).decode('utf-8')
    g = group.serialize(g).decode('utf-8')
    data.write(e_decode+'\n'+str(c)+'\n'+str(z)+'\n'+public_info+'\n'+g)
    
'''
with open(uc_data_path, 'r') as readata:
    list = []
    for line in readata:
        list.append(line.strip())
    e  = group.deserialize(list[0].encode('utf-8'))
    c = int(list[1])
    z = int(list[2])
    public_info = group.deserialize(list[3].encode('utf-8'))
    print(public_info)
    zkproof_real = Proof(e, c, z)
    #print(zkproof_real)
    verify = zkp_verify(zkproof_real, public_info,1) 
    if verify == 1 :
        print('1')
'''
# yeu cau verify den fog
#run_client('0')       
 
