# import pandas as pd

# # Create a pandas dataframe from your dataset file(s)
# df = pd.read_json(...) # or any other way

# # Save the file in the Parquet format
# df.to_parquet("dataset.parquet", row_group_size=100, engine="pyarrow", index=False)
from datasets import load_dataset

# 下载数据集
# dataset = load_dataset('nilq/small-lua-stack')#CodeTranslatorLLM/Code-Translation
dataset = load_dataset('CodeTranslatorLLM/Code-Translation')#CodeTranslatorLLM/Code-Translation
# 查看数据集信息
print(dataset)

# 访问数据集内容
train_data = dataset['train']
test_data = dataset['test']

# 使用数据集进行进一步处理或分析
# ...