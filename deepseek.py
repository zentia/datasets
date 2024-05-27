import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import fnmatch
import json
import gc
import logging

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)   # 设置打印级别
formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s')
 
# 设置屏幕打印的格式
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

log_path = 'test.log'
output_path = 'output.txt'
# 设置log保存
if os.path.isfile(log_path): 
  os.remove(log_path)
fh = logging.FileHandler(log_path, encoding='utf8')
fh.setFormatter(formatter)
logger.addHandler(fh)
 
 
execute_files = []

with open(output_path, 'r', encoding='utf-8') as file:
  execute_files = file.readlines()

def find_lua_files(root_dir):
    lua_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if fnmatch.fnmatch(file, '*.lua'):
                path = os.path.join(root, file)
                if path not in execute_files:
                  lua_files.append(path)
    return lua_files

def read_lua_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def change_file_extension(file_path, new_extension):
    # 获取文件名和旧后缀名
    file_name, old_extension = os.path.splitext(file_path)
    
    # 构建新的文件路径
    new_file_path = file_name + new_extension
        
    return new_file_path


# 指定新的后缀名
new_extension = '.mts'


# 指定要遍历的文件夹路径
folder_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/RawAssets/LuaScripts'

# 调用函数获取所有Lua文件
lua_files = find_lua_files(folder_path)

device = "cuda" # the device to load the model onto
# model_id = "aiXcoder/aixcoder-7b-base"
model_id = "deepseek-ai/deepseek-coder-1.3b-base"
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_id)

def reasoning_segment(content:str, responses:list):
  array = content.splitlines()
  index = len(array)//2
  for i in range(index, len(array)):
    line = array[i]
    if line == 'end':
        index = i
        break
  a = array[:index+1]
  b = array[index+1:]
  content_a = '\n'.join(a)
  response_a = reasoning_element(content_a)
  if response_a is None:
     reasoning_segment(content_a,responses)
  else:
     responses.append(response_a)
  content_b = '\n'.join(b)
  response_b = reasoning_element(content_b)
  if response_b is None:
     reasoning_segment(content_b, responses)
  else:
     responses.append(response_b)
  pass

def reasoning_element(prompt:str):
  input_text = f'{prompt}\n目标语言：TypeScript'
  inputs = tokenizer(input_text, return_tensors="pt").to(device)
  gc.collect()
  torch.cuda.empty_cache()
  # 关闭梯度计算
  # with torch.no_grad():
  try:
    # 使用模型的generate方法进行文本生成
    outputs = model.generate(        **inputs,        max_new_tokens=8192*2,        temperature=0.1,        top_p=0.1,        top_k=40,        do_sample=True,        num_return_sequences=3    )
    if outputs is None:
        print('generated_ids is None')
        return
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    array = response.splitlines()
    # return array
    begin = 1
    for i in range(len(array) - 1):
      if array[i+1] == '```typescript':
          begin = i+2
      if array[i+1] == '```':
          return array[begin:i+1]
  except RuntimeError as e:
      if "out of memory" in str(e):
        gc.collect()
        torch.cuda.empty_cache()  
        print(str(e))
        return

def write_file(path:str,data:list, new_extension:str):
  path = change_file_extension(path, new_extension)
  f = open(path, "w", encoding="utf-8")
  f.write('\n'.join(data))
  f.close()      
  pass

ignores = [
   "Generated",
   "Debugger",
   "Import",
   "Log.lua",
   "Boot",
   "cpp2lua_common",
   "AssetDeclare",
   "Object",
   "AsynchronousLoader",
   'DateTimeService',
   'FrameChaseUp',
   'FrameCommandService',
   'LuaEventID',
   'DeviceCheckService',
   'CommonDefine',
   'UIUtility',
   'UIJumpProcesser',
   'RelationHelper',
   'GameCoreBattleBuilderBase',
   'BeginloadService',
   'Gameplay',
   'StandardPreloadConfig',
   'LordChooseGameplay',
   'GameSayService',
   'UIGmInputItem',
   '_AutoBind.lua'
]

segment_files = [
   'GMBattle',
   'GMDefine',
   'RankBattle'
]


def reasoning(file:str, force:bool):
  # ignore file
  for val in ignores:
     if val in file:
        return
  for val in segment_files:
     if val in file:
        return
  if file not in execute_files:
    execute_files.append(file)
    write_file('output', execute_files, '.txt')
  path = str.replace(file, 'RawAssets/LuaScripts','DevAssets/TypeScript_AI/src',1)
  temp = change_file_extension(path, new_extension)
  if os.path.exists(temp) and not force:
      return
  logging.info(path)
  prompt = read_lua_file(file)
  directory = os.path.dirname(path)
  if not os.path.exists(directory):
      os.makedirs(directory)
  response = reasoning_element(prompt)
  if response is None:
    response = []
    reasoning_segment(prompt, response)
    data = []
    for index, item in enumerate(response):
      write_file(path,item,f'{index}{new_extension}')
      if index > 0:
         for j, line in enumerate(item):
            if 'public' in line and 'constructor' not in line:
              if index == len(response) - 1:
                 data.append('\n'.join(item[j:]))
              else:
                data.append('\n'.join(item[j:len(item)-1]))
              break   
      else:
         data.append('\n'.join(item[:len(item)-1]))
    write_file(path,data,new_extension)
  else:
    write_file(path,response,new_extension)
  
  

for file in lua_files:
    reasoning(file,False)
# reasoning('/media/liyanfeng/2TM2/OSCE_0704/Project/RawAssets/LuaScripts/Logic/UIComponents/CMList.lua', True)
