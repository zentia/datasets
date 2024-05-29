import os
import common
import shutil


if __name__ == '__main__':
  current_directory = os.getcwd()

  target_dirs = current_directory + '/../output/typescript'

  ts_root_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/DevAssets/TypeScript/src/system/ui-system'

  for root, dirs, files in os.walk(target_dirs):
    for file in files:
      if '@' in file:
        continue
      file_name_without_extension = os.path.splitext(file)[0]      
      ts_file_name = file_name_without_extension + '.mts'
      path = os.path.join(root, ts_file_name)
      relative_path = os.path.relpath(path,target_dirs)
      ts_relative_path = common.convert_path_to_snake_case(relative_path)
      ts_path = os.path.join(ts_root_path,ts_relative_path)
      directory_path = os.path.dirname(ts_path)
      if not os.path.exists(directory_path):
        os.makedirs(directory_path, True)
      shutil.copyfile(os.path.join(root,file),ts_path)
      print(ts_path)

