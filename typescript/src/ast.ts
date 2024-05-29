import * as fs from 'fs';
import * as path from 'path';
import { mergeSourceFiles } from './mergeClasses';


function traverseDirectory(dir: string, tsMap: Map<string, string[]>): void {
    try {
        const files = fs.readdirSync(dir, { withFileTypes: true });

        files.forEach(file => {
            const fullPath = path.join(dir, file.name);
            if (file.isDirectory()) {
                traverseDirectory(fullPath, tsMap);
            } else {
                if (fullPath.includes('@')) {
                    const name = fullPath.split('@')[0];
                    let list = tsMap.get(name);
                    if (!list) {
                        list = [fullPath];
                        tsMap.set(name, list);
                    } else {
                        list.push(fullPath);
                    }
                }
            }
        });
    } catch (err) {
        console.error(`Error reading directory ${dir}: ${err}`);
    }
}

export function testAst(){
    const tsDirs = '/media/liyanfeng/8T/datasets/output/typescript/Prize';
    const tsMap = new Map<string, string[]>();
    traverseDirectory(tsDirs, tsMap);
    
    tsMap.forEach((value, key) => {

        const outputPath = `${key}.mts`;
        mergeSourceFiles(value,outputPath);
//         value.forEach(fileName=>{
// // Parse a file
// const sourceFile = ts.createSourceFile(fileName,readFileSync(fileName).toString(), ts.ScriptTarget.ES2015);
// // delint(sourceFile);
// printRecursiveFrom(sourceFile,0,sourceFile);
//         })
        
        
    });
}