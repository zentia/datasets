import random

class MyDataset:
    def __init__(self, data):
        self.data = data

    def split_dataset(self, train_ratio, val_ratio, test_ratio):
        # 计算划分的样本数量
        total_samples = len(self.data)
        train_samples = int(total_samples * train_ratio)
        val_samples = int(total_samples * val_ratio)
        test_samples = total_samples - train_samples - val_samples

        # 随机打乱数据集
        random.shuffle(self.data)

        # 划分数据集
        train_data = self.data[:train_samples]
        val_data = self.data[train_samples:train_samples+val_samples]
        test_data = self.data[train_samples+val_samples:]

        return train_data, val_data, test_data
    

