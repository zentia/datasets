from datasets import load_dataset
import json
import jsonlines

# 下载数据集
# dataset = load_dataset('nilq/small-lua-stack')
dataset = load_dataset('CodeTranslatorLLM/Code-Translation')

# 获取数据集内容
data = dataset['train']  # 这里以训练集为例，你可以根据需要选择其他分割

# 将数据集内容转换为Python字典或列表
# data_dict = data.to_dict()  # 转换为字典
# 或者
# data_list = data.to_pandas()  # 转换为列表

# 将数据集内容逐行写入JSON文件
with jsonlines.open('output.jsonl', 'w') as writer:
    for item in data:
        writer.write(item)