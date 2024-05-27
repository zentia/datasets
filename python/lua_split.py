import subprocess
import sys
import os
from common import change_file_extension, clear_folder, convert_to_utf8, convert_path_to_snake_case
import shutil

working_directory = '/media/liyanfeng/1TSata/trunk_proj/Tools/osg-dev-kit/lsp-server'
output_directory = ''

if sys.platform.startswith('win'):
   working_directory = 'F:/trunk_proj/Tools/osg-dev-kit/lsp-server'
   output_directory = 'D:/datasets/output/lua'

def extract_file(lua_file:str,method:str,ctor:str,flag:int):
    """
    :param flag: 1表示罗列函数列表输出extract_methods.txt，0表示输出函数内容输出文件extract_file.txt
    """
    arg = '-func={},{}'.format(ctor,method) if ctor else '-func={}'.format(method)
   #  process = subprocess.Popen(['java','-jar','LuaExtractor-2.jar','-filePath='+lua_file,arg,'-drop_decl','-list=1'], cwd=working_directory, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process = subprocess.Popen(['java','-jar','LuaExtractor-2.jar','-filepath={}'.format(lua_file),arg,'-drop_decl','-list={}'.format(flag)], cwd=working_directory, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # 获取输出和错误
    stdout, stderr = process.communicate()
    # 打印输出
    print(stdout.decode())

    # 检查是否有错误
    if process.returncode != 0:
       print(stderr.decode())

def copyfile(root:str, src_directory_len:int,file:str,path:str):
   relation_dir = root[src_directory_len+1:]
   dir = os.path.join(output_directory, relation_dir)
   if not os.path.exists(dir):
      os.makedirs(dir, True)
   output_path = os.path.join(dir, file)
   with open(path, 'r', encoding='gbk') as src, open(output_path, 'w', encoding='utf-8') as dst:
      shutil.copyfileobj(src, dst)

def find_missing_files():
   src_directory = r'F:\trunk_proj\Project\RawAssets\LuaScripts\Logic\UISystem'
   src_directory_len = len(src_directory)
   target_directory = r'G:\OSCE_0704\Project\DevAssets\TypeScript\src\system\ui-system'
   target_directory_len = len(target_directory)
   extract_methods_path = os.path.join(working_directory,'extract_methods.txt')
   extract_file_path = os.path.join(working_directory, 'extract_file.txt')
   clear_folder(output_directory)
   for root, dirs, files in os.walk(src_directory):
      for file in files:
         if file.endswith('_AutoBind.lua'):
            continue

         path = os.path.join(root, file)
         relation_path = path[src_directory_len+1:]
         relation_path = change_file_extension(relation_path, '.mts')
         ts_path = convert_path_to_snake_case(relation_path)
         ts_path = os.path.join(target_directory, ts_path)
         if os.path.exists(ts_path):
            continue
         extract_file(path,'','',1)
         if os.path.exists(extract_methods_path):
            with open(extract_methods_path,'r',encoding='utf-8') as f:
               lines = f.readlines()
               length = len(lines)
               if length > 0:
                  ctor=''
                  if lines[0].endswith('ctor\n'):
                     ctor=lines[0][:-1]
                  for i in range(1, length):
                     method=lines[i][:-1]
                     extract_file(path,method,ctor,0)
                     if os.path.exists(extract_file_path):
                        method_sign = method.split(':')[1]
                        relation_dir = root[src_directory_len+1:]
                        dir = os.path.join(output_directory, relation_dir)
                        if not os.path.exists(dir):
                           os.makedirs(dir, True)
                        output_path = os.path.join(dir, file)
                        target_path = change_file_extension(output_path, '@{}.lua'.format(method_sign))
                        with open(extract_file_path, 'r', encoding='gbk') as src, open(target_path, 'w', encoding='utf-8') as dst:
                           shutil.copyfileobj(src, dst)
               else:
                  copyfile(root,src_directory_len,file,path)
            os.remove(extract_methods_path)             
         else:
            exit(-1)

    
if __name__ == '__main__':
   # extract_file(r'F:\trunk_proj\Project\RawAssets\LuaScripts\Logic\UISystem\Libraries\UI\UIHeroDetailInfoShowData.lua','UIHeroDetailInfoShowDataClass:Reset','UIHeroDetailInfoShowDataClass:ctor',0)
   # extract_file(r'Logic\UISystem\Libraries\UI\UIHeroDetailInfoShowData.lua','UIHeroDetailInfoShowDataClass:Reset','',0)
   find_missing_files()
   pass