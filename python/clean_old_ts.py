import os

if __name__ == '__main__':
    ts_root_path = '/media/liyanfeng/2TM2/OSCE_0704/Project/DevAssets/TypeScript/src/system/ui-system'

    for root, dirs, files in os.walk(ts_root_path):
        for file in files:
            pass