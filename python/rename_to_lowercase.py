import re
import os

def camel_to_snake(name):
    # 将驼峰命名转换为连字符连接的小写形式
    name = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1-\2', name).lower()
    return name

def convert_path_to_snake_case(path):
    # 分割路径为单独的部分
    parts = path.split(os.sep)
    # 转换每个部分为小写连字符连接形式
    converted_parts = [camel_to_snake(part) for part in parts]
    # 重新组合路径
    converted_path = os.sep.join(converted_parts)
    return converted_path.replace('_','-').replace('--','-')

# 示例使用
original_path = 'GMCS2Lua'
converted_path = convert_path_to_snake_case(original_path)
print(converted_path)  # 输出: some/path/with/camel-case-file-names