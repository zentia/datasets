import * as path from 'path';

export function getFileNameWithoutExtension(filePath: string): string {
    const baseName = path.basename(filePath);
    const extName = path.extname(filePath);
    return baseName.slice(0, -extName.length);
}

export function removeTrailingSubstring(str: string, suffix: string): string {
    if (str.endsWith(suffix)) {
        return str.slice(0, -suffix.length);
    }
    return str;
}

if (require.main == module) {
    // const filePath = '/path/example.txt';
    // console.log(getFileNameWithoutExtension(filePath));

    
    // 示例用法
    const originalString = "UIAdvancedLordNameClass";
    const suffix = "Class";
    const result = removeTrailingSubstring(originalString, suffix);
    console.log(result); // 输出: "Hello"

}