import os
import json
from common import convert_path_to_snake_case, change_file_extension

def generate(callback):
    # 指定要遍历的文件夹路径
    lua_folder_path = '/media/liyanfeng/1TSata/trunk_proj/Project/RawAssets/LuaScripts/Logic/UISystem'
    lua_folder_path_len = len(lua_folder_path)
    ts_folder_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/DevAssets/TypeScript/src/system/ui-system'

    for root, dirs, files in os.walk(lua_folder_path):
        relation_dir = root[lua_folder_path_len+1:]
        for file in files:
            relation_path = os.path.join(relation_dir, file)
            ts_relation_path = change_file_extension(relation_path, '.mts')
            ts_relation_path = convert_path_to_snake_case(ts_relation_path)
            ts_path = os.path.join(ts_folder_path, ts_relation_path)
            if os.path.exists(ts_path):
                lua_path = os.path.join(root, file)
                with open(ts_path, 'r', encoding='utf-8') as ts_file, open(lua_path, 'r', encoding='utf-8') as lua_file:
                    callback(lua_file.read(), ts_file.read())