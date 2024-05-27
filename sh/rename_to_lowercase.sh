#!/bin/bash

# 函数：将驼峰命名转换为小写，并用连字符替换大写字母
camel_to_snake() {
    local name="$1"

    # 首先，处理特殊的白名单单词，将它们转换为小写
    name=$(echo "$name" | sed -e 's/\(BP\)/bp/g' -e 's/\(UI\)/ui/g' -e 's/\(DB\)/db/g' -e 's/\(AI\)/ai/g' -e 's/\(PVP\)/pvp/g' -e 's/\(GM\)/gm/g' -e 's/\(MSDK\)/msdk/g' -e 's/\(SDK\)/sdk/g' -e 's/\(CG\)/cg/g' -e 's/\(CM\)/cm/g' -e 's/\(3D\)/3d/g' -e 's/\(OB\)/ob/g')

    # 然后，将剩余的驼峰命名转换为小写连字符连接形式
    name=$(echo "$name" | sed -r 's/([a-z0-9])([A-Z])/\1-\L\2/g')

    # 转换为小写
    echo "$name" | tr '[:upper:]' '[:lower:]'
}

# 函数：递归地重命名目录和文件
rename_files() {
    local path="$1"
    for entry in "$path"/*; do
        # 获取原始文件/目录名
        local original_name=$(basename "$entry")
        # 特殊文件名处理
        if [ "$original_name" == "Init.mts" ]; then
            mv -v "$entry" "$(dirname "$entry")/index.mts"
            continue
        fi
        # 转换为小写并替换驼峰命名
        local new_name=$(camel_to_snake "$original_name")
        # 如果新旧名称不同，则重命名
        if [ "$original_name" != "$new_name" ]; then
            mv -v "$entry" "$(dirname "$entry")/$new_name"
        fi
        # 如果是目录，则递归处理
        if [ -d "$(dirname "$entry")/$new_name" ]; then
            rename_files "$(dirname "$entry")/$new_name"
        fi
    done
}


# 从当前目录开始处理
rename_files /media/liyanfeng/2TM2/OSCE_0704/Project/DevAssets/TypeScript_AI/src/system/Logic