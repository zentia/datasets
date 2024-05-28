import * as path from 'path';

export function getFileNameWithoutExtension(filePath: string): string {
    const baseName = path.basename(filePath);
    const extName = path.extname(filePath);
    return baseName.slice(0, -extName.length);
}

if (require.main == module) {
    const filePath = '/path/example.txt';
    console.log(getFileNameWithoutExtension(filePath));
}