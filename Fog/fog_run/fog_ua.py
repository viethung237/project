import sys
sys.path.insert(0, '/home/hung/project')
fog_ua_path = '/home/hung/project/Fog/fog_data/ua_data_att.txt'
fog_uc_path = '/home/hung/project/Fog/fog_data/uc_data_att.txt'
from zkp_abe.access_tree import *
import json
from server.server_run.sever import runserver
#runserver('0')
#fog gen policy
with open(fog_ua_path,'r+') as ua_att:
    input_mapping_ua = json.loads(ua_att.read())
    tree_root = create_tree(input_mapping_ua)
    ua_att.seek(0)
    ua_att.write(tree_to_dict(tree_root))
