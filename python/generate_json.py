import json
from generate import generate

# 创建一个字典，用于存储Lua文件内容
contents = []

def fill(lua_file, ts_file):
    contents.append({
        "instruction":lua_file,
        "input":"",
        "output":ts_file})        

if __name__ == '__main__':
    generate(fill)
    # 将字典内容输出到JSON文件
    output_file = '/media/liyanfeng/8T/datasets/output/lua_to_typescript.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(contents, file, indent=4, ensure_ascii=False)

    print("文件内容已成功输出到JSON文件中。")
