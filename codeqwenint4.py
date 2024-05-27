import fnmatch
import os
from modelscope import AutoModelForCausalLM, AutoTokenizer
device = "cuda" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained(
    "huangjintao/CodeQwen1.5-7B-Chat-GPTQ-Int4",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("huangjintao/CodeQwen1.5-7B-Chat-GPTQ-Int4")

# 指定要遍历的文件夹路径
folder_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/RawAssets/LuaScripts'


def find_lua_files(root_dir):
    lua_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if fnmatch.fnmatch(file, '*.lua'):
                path = os.path.join(root, file)
                lua_files.append(path)
    return lua_files

# 调用函数获取所有Lua文件
lua_files = find_lua_files(folder_path)

prompt = "Write a quicksort algorithm in python."
messages = [
    {"role": "system", "content": "Lua翻译成TypeScript"},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(device)

generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response)