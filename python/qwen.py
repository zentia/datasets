# env aixcoder-7b
from modelscope import AutoModelForCausalLM, AutoTokenizer
import os
import fnmatch
import logging
from accelerate import infer_auto_device_map, init_empty_weights
from modelscope import AutoConfig, AutoModelForCausalLM
from peft import PeftModel
from peft import LoraConfig, TaskType, get_peft_model
import common
import sys


working_directory = '/media/liyanfeng/1TSata/trunk_proj/Tools/osg-dev-kit/lsp-server'

def execute_segment(path:str):
    # path='Logic/UISystem/PVPSettle/PVPSettleModule.lua'
    get_method(lua_file=path)
    prompts=[]
    methods=[]
    with open(working_directory+'/extract_methods.txt','r',encoding='utf-8') as file:
        content = file.readlines()
        contain_ctor = False
        for method in content:
            m:str = method.split(':')[1].strip('\n')
            if m == 'ctor':
               contain_ctor=True
               continue
            prompt=extract_file(lua_file=path,method=m.strip('\n'),ctor=contain_ctor)
            prompts.append(prompt)
            methods.append(m)
    return prompts,methods

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
# if os.path.isfile(output_path):
#     with open(output_path, 'r', encoding='utf-8') as file:
#         execute_files = file.readlines()

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


# 指定新的后缀名
new_extension = '.mts'


# 指定要遍历的文件夹路径
lua_root_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/RawAssets/LuaScripts/Logic'
ts_root_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/DevAssets/TypeScript_AI/src/system/logic'

# 调用函数获取所有Lua文件
lua_files = find_lua_files(lua_root_path)

device = "cuda" # the device to load the model onto

model_id = "qwen/CodeQwen1.5-7B-Chat"
lora_path = '../output/CodeQwen1.5/checkpoint-500/'

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto"
)

config = LoraConfig(
    task_type=TaskType.CAUSAL_LM, 
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=False, # 训练模式
    r=8, # Lora 秩
    lora_alpha=32, # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.1# Dropout 比例
)
# 加载lora权重
model = PeftModel.from_pretrained(model, model_id=lora_path, config=config)

def reasoning_segment(prompts:list, methods:list,path:str):
    for index, prompt in enumerate(prompts):
        response = reasoning_element(prompt)
        write_file(path=path,data=response,new_extension=methods[index]+new_extension)
    

def reasoning_element(prompt:str):
  messages = [
      {"role": "system", "content": "Lua翻译成TypeScript，规则如下：1.所有的赋值为false的语句是未定义行为。2.ctor是构造函数，需要声明并定义里面的成员，翻译其它函数的时候不要补充成员定义。3.uid是的类型是bigint。4.不要定义返回值类型。5.忽略auto_bind()函数。"},
      {"role": "user", "content": prompt}
  ]
  
  text = tokenizer.apply_chat_template(
      messages,
      tokenize=False,
      add_generation_prompt=True
  )
  model_inputs = tokenizer([text], return_tensors="pt").to(device)
  # 关闭梯度计算
  # with torch.no_grad():
  # 使用模型的generate方法进行文本生成
  generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=1024*1
  )
  generated_ids = [
      output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
  ]

  response:str = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
  index = response.find('\nuser')
  if index != -1:
     return response[:index]
  return response
        

def write_file(path:str,data:str, new_extension:str):
  path = change_file_extension(path, new_extension)
  f = open(path, "w", encoding="utf-8")
  f.write(data)
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
   '_AutoBind.lua',
   'RankBattle.lua',
   'PVPSettleDataInstance.lua'
]

segment_files = [
   'PVPSettleModule',
   'RankBattle'
]


def reasoning(file:str, force:bool):
    # ignore file
    for val in ignores:
        if val in file:
            return
    
    relative_path = os.path.relpath(file,lua_root_path)
    if relative_path.endswith('Init.lua'):
        relative_path = relative_path[:-8] + 'index.mts'
    path = str.replace(file, 'RawAssets/LuaScripts/Logic','DevAssets/TypeScript_AI/src/system/logic',1)
    temp = change_file_extension(relative_path, new_extension)
    temp = python.rename_to_lowercase.convert_path_to_snake_case(temp)
    temp = os.path.join(ts_root_path,temp)
    if os.path.exists(temp) and not force:
        return
    logging.info(temp)
    for segment in segment_files:
        if segment in file:
            prompts, methods = execute_segment(file)
            reasoning_segment(prompts, methods,path)
            return
    prompt = read_lua_file(file)
    if len(prompt) == 0:
        return
    if prompt.isspace():
        return 
    directory = os.path.dirname(temp)
    if not os.path.exists(directory):
        os.makedirs(directory)
    response = reasoning_element(prompt)
    write_file(temp,response,new_extension)    

    
# python .\qwen.py D:/datasets/output/lua/nts
if __name__ == '__main__':
    ts_dirs = '../output/typescript'
    lua_dirs = '../output/lua'
    args = sys.argv[1:]
    if len(args) == 1:
        lua_dirs = args[0]
        print(lua_dirs)
    else:
        common.clear_folder(ts_dirs)
    for root, dirs, files in os.walk(lua_dirs):
        for file in files:
            path = os.path.join(root, file)
            with open(path,'r',encoding='utf-8') as lua:
                response = reasoning_element(lua.read())
                ts_path = path.replace('/output/lua','/output/typescript')
                ts_path = ts_path.replace('.lua','.mts')
                ts_root = root.replace('/output/lua','/output/typescript')
                os.makedirs(ts_root, exist_ok=True)
                print(ts_path)
                with open(ts_path, 'w', encoding='utf-8') as ts:
                    ts.write(response)
