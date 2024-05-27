import shutil
import os
import codecs
import psutil
import re

def change_file_extension(file_path, new_extension):
    # 获取文件名和旧后缀名
    file_name, old_extension = os.path.splitext(file_path)
    
    # 构建新的文件路径
    new_file_path = file_name + new_extension
        
    return new_file_path


def clear_folder(folder_path):
    # 遍历文件夹
    for filename in os.listdir(folder_path):
        # 获取文件或目录的绝对路径
        file_path = os.path.join(folder_path, filename)
        try:
            # 判断是否为文件夹
            if os.path.isdir(file_path):
                # 删除文件夹及其内容
                shutil.rmtree(file_path)
            else:
                # 删除文件
                os.remove(file_path)
        except Exception as e:
            print(f"Error while deleting {file_path}: {e}")


def convert_to_utf8(input_file, output_file, input_encoding):
    with codecs.open(input_file, 'r', encoding=input_encoding) as infile:
        content = infile.read()

    with codecs.open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def get_process_id_using_file(file_path):
    for process in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            if process.info['open_files']:
                for file in process.info['open_files']:
                    if file.path == file_path:
                        return process.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return None

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
    converted_path = converted_path.replace('_','-').replace('--','-')
    if converted_path.endswith(f'init.mts'):
        return converted_path[:-8] + 'index.mts'
    return converted_path


if __name__ == '__main__':
    # 使用示例
    # folder_path = "D:/datasets/output/lua"
    # clear_folder(folder_path)

    # # 使用示例
    # input_file = 'path/to/your/input_file'
    # output_file = 'path/to/your/output_file'
    # input_encoding = 'your_input_encoding'  # 例如：'gbk', 'big5', 'cp1252'等

    # convert_to_utf8(input_file, output_file, input_encoding)

    # # 使用示例
    # file_path = 'path/to/your/file'
    # process_id = get_process_id_using_file(file_path)

    # if process_id:
    #     print(f"Process ID using the file: {process_id}")
    # else:
    #     print("No process found using the file.")

    # 示例使用
    original_path = 'GMCS2Lua'
    converted_path = convert_path_to_snake_case(original_path)
    print(converted_path)  # 输出: some/path/with/camel-case-file-names