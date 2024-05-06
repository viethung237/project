import sys
sys.path.insert(0, '/home/hung/project')
fog_ua_path = '/home/hung/project/Fog/fog_data/ua_data_att.txt'
fog_uc_path = '/home/hung/project/Fog/fog_data/uc_data_att.txt'
from zkp_abe.access_tree import *
import json
#from server.server_run.sever import runserver
#runserver('0')
#fog gen policy khi nhan att tu uc
with open(fog_uc_path,'r') as uc_att:
    input_mapping_uc = json.loads(uc_att.read())
    with open(fog_ua_path,'r+') as ua_att:
        tree_dict = ua_att.read()
        tree_root = dict_to_tree(tree_dict)
        key1 = list(input_mapping_uc.keys())[0]
        subtree_root = create_subtree_from_leaf(tree_root, key1, input_mapping_uc)
        ua_att.seek(0)
        print(print_tree(tree_root))
        ua_att.write(tree_to_dict(tree_root))



    