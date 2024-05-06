from random import randint
from Crypto.Hash import SHA256
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
group = PairingGroup('SS512')

def int_to_bytes(number):
    byte_length = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_length, byteorder='big')
 
class Proof:
    def __init__(self, encrypted_random, c: int, z: int):
        self.encrypted_random = encrypted_random
        self.c = c
        self.z = z
   
    def display(self):
        #print("Encrypted random: ")
        self.encrypted_random.display()
        #print("c = ", self.c)
        #print("z = ", self.z)
 
def zkp_generate(secret_info: int, ID: int):
    # random r and calc r*G
    g = group.random(G1)
    r = randint(pow(2,254), pow(2,256))
    encrypted_r = g ** r
 
    # x*G
    public_info = g ** secret_info
 
    # challenge c = H(ID,g,g^r, g^x)
    c_bytes = SHA256.new(int_to_bytes(ID) + group.serialize(g) + group.serialize(encrypted_r) + group.serialize(public_info)).digest()
    #print('bf0', int_to_bytes(ID) + group.serialize(g) + group.serialize(encrypted_r) + group.serialize(public_info))
    #print('bf',c_bytes)
    c_int = int.from_bytes(c_bytes, byteorder='big')
    z = r + c_int * secret_info
 
    return encrypted_r, c_int, z, g
 
def zkp_verify(proof: Proof, public_info, ID: int, g):
    # Read value from received proof
    receive_encrypted_r = proof.encrypted_random
    receive_c = proof.c
    receive_z = proof.z
    # check if c is calculated correctly
    c_hash = SHA256.new(int_to_bytes(ID) + group.serialize(g) + group.serialize(receive_encrypted_r) + group.serialize(public_info)).digest()
    #print('at0',int_to_bytes(ID) + group.serialize(g) + group.serialize(receive_encrypted_r) + group.serialize(public_info))
    #print('at',c_hash)
    if receive_c == int.from_bytes(c_hash, byteorder='big'):
        
        lhs = g ** receive_z
        rhs = receive_encrypted_r * (public_info ** receive_c)
        # verify proof z (z*G =? r*G + c*x*G)\
        #print('1')
        if lhs == rhs:
            #print("Valid proof")
            return True
    #print("Invalid proof")
    return False
'''
real_info = 345
fake_info = 344
e, c, z,g = zkp_generate(real_info,1)
public_info = g ** real_info

#print('e' ,e,'\n')
#print('c',c,'\n')
#print(z)

zkproof_real = Proof(e, c, z)
verify = zkp_verify(zkproof_real, public_info,1,g) 
print(verify)
'''
