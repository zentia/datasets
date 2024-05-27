import os
import fnmatch
import json

def find_lua_files(root_dir):
    lua_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if fnmatch.fnmatch(file, '*.lua'):
                lua_files.append(os.path.join(root, file))
    return lua_files

def find_ts_files(root_dir):
    ts_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if fnmatch.fnmatch(file, '*.ts'):
                ts_files.append(os.path.join(root, file))
    return ts_files

def read_lua_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def read_ts_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def change_file_extension(file_path, new_extension):
    # 获取文件名和旧后缀名
    file_name, old_extension = os.path.splitext(file_path)
    
    # 构建新的文件路径
    new_file_path = file_name + new_extension
        
    return new_file_path

# 指定要遍历的文件夹路径
lua_folder_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/RawAssets/LuaScripts'

ts_folder_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/DevAssets/TypeScript_AI/src'

# 调用函数获取所有Lua文件
lua_files = find_lua_files(lua_folder_path)

ts_files = find_ts_files(ts_folder_path)

# 创建一个字典，用于存储Lua文件内容
contents = []

# 读取每个Lua文件的内容并存储到字典中
for file in lua_files:
    lua_content = read_lua_file(file)
    path = str.replace(file,'RawAssets/LuaScripts','DevAssets/TypeScript_AI/src')
    path = change_file_extension(path, '.mts')
    if os.path.exists(path):
        ts_content = read_ts_file(path)
        if ts_content is None:
            continue
        contents.append({
            "instruction":lua_content,
            "input":"",
            "output":ts_content})

# 将字典内容输出到JSON文件
output_file = '/media/liyanfeng/8T/self-llm/dataset/lua_to_typescript.json'
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(contents, file, indent=4, ensure_ascii=False)

print("文件内容已成功输出到JSON文件中。")
