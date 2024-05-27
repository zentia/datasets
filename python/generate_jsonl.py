import jsonlines
from generate import generate


if __name__ == '__main__':
    # 将字典内容输出到JSON文件
    output_file = '/media/liyanfeng/8T/datasets/output/lua_to_typescript.jsonl'
    with jsonlines.open(output_file, mode='w') as writer:
        def fill(lua_file, ts_file):
            writer.write({
            "instruction":'Lua翻译成TypeScript',
            "input":lua_file,
            "output":ts_file})
        generate(fill)
        

    print("文件内容已成功输出到jsonl文件中。")
