import re
import os

# Lua文件路径
lua_file_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/RawAssets/LuaScripts/Logic/UISystem/Operation/Impl/OperationInvite.lua'

# 输出目录
output_dir = './output/lua'
os.makedirs(output_dir, exist_ok=True)

# 读取Lua文件内容
with open(lua_file_path, 'r') as file:
    lua_content = file.readlines()

# 函数开始和结束标记
function_start = 'function '
end_keyword = 'end'

# 用于存储函数的字典
functions = {}

# 当前函数名和函数体
current_function = None
function_body = []
function_depth = 0

# 解析文件
for line in lua_content:
    if function_start in line:
        function_depth += 1
        if function_depth == 1:
            current_function = re.findall(r'function\s+([A-Za-z0-9_]+:[A-Za-z0-9_]+)', line)[0]
            function_body = [line]
            continue
    if end_keyword in line:
        function_body.append(line)
        function_depth -= 1
        if function_depth == 0 and current_function:
            functions[current_function] = function_body
            current_function = None
            function_body = []
        continue
    if current_function:
        function_body.append(line)

# 将每个函数写入单独的文件
for func_name, func_body in functions.items():
    # 生成文件名
    file_name = func_name.split(':')[-1] + '.lua'
    file_path = os.path.join(output_dir, file_name)

    # 写入文件
    with open(file_path, 'w') as lua_file:
        lua_file.writelines(func_body)

print(f'Found and extracted {len(functions)} functions.')