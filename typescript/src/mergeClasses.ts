import * as ts from 'typescript';
import * as fs from 'fs';
import * as path from 'path';
import { logMessage } from './log';

function readSourceFile(filePath: string): ts.SourceFile {
  const sourceCode = fs.readFileSync(filePath, 'utf8');
  return ts.createSourceFile(filePath, sourceCode, ts.ScriptTarget.Latest, true);
}

function mergeClasses(classes: ts.ClassDeclaration[], sourceFiles: ts.SourceFile[]): [ts.ClassDeclaration, ts.SourceFile] {
  if (classes.length === 0) {
    throw new Error('No classes to merge');
  }

  const baseClass = classes[0];
  const baseClassSourceFile = sourceFiles[0];
  const mergedMembers: ts.ClassElement[] = [];
  const mergedTextMembers: string[] = [];

  const memberMap = new Map<string, ts.ClassElement>();
  const memberTextMap = new Map<string, string>();
  let ctor = false;
  for (let i = 0; i < classes.length; i++) {
    const cls = classes[i];
    const sourceFile = sourceFiles[i];
    
    cls.members.forEach(member => {
        if ((ts.isMethodDeclaration(member)) && member.name && ts.isIdentifier(member.name)) {
          if (!memberMap.has(member.name.text)) {
            memberMap.set(member.name.text, member);
          }
          if (!memberTextMap.has(member.name.text)) {
              memberTextMap.set(member.name.text, member.getText(sourceFile))
          }
        } else {
            if (ts.isConstructorDeclaration(member)) {
                if (ctor)
                    return;
                ctor = true;
            }
          mergedMembers.push(member);
            mergedTextMembers.push(member.getText(sourceFile));
        }
      });
  }

  mergedMembers.push(...memberMap.values());
  mergedTextMembers.push(...memberTextMap.values());
  let resultFile:ts.SourceFile|undefined = undefined;
  baseClass.forEachChild(node=>{
    if (node.kind == ts.SyntaxKind.Identifier) {
        
        resultFile = ts.createSourceFile('', `/* eslint-disable camelcase */\n/* eslint-disable @typescript-eslint/naming-convention */\nexport class ${node.getText(baseClassSourceFile)}\{\n${mergedTextMembers.join('\n')}\n\}`, ts.ScriptTarget.Latest, false, ts.ScriptKind.TS);
        
    }
  })
  

  return [ts.factory.createClassDeclaration(
    baseClass.modifiers,
    baseClass.name,
    baseClass.typeParameters,
    baseClass.heritageClauses,
    mergedMembers
  ), resultFile!];
}

export function mergeSourceFiles(filePaths: string[], outputFile: string): void {
  const sourceFiles = filePaths.map(readSourceFile);

  const classMap = new Map<string, ts.ClassDeclaration[]>();
  const classSourceMap = new Map<string, ts.SourceFile[]>();
  sourceFiles.forEach(sourceFile => {
    sourceFile.statements.forEach(statement => {
      if (ts.isClassDeclaration(statement) && statement.name) {
        const className = statement.name.text;
        if (!classMap.has(className)) {
          classMap.set(className, []);
        }
        
        classMap.get(className)!.push(statement);
        if (!classSourceMap.has(className)) {
            classSourceMap.set(className, []);
        }
        classSourceMap.get(className)!.push(sourceFile);
      }
    });
  });

  const mergedClasses: ts.ClassDeclaration[] = [];
  const mergedSourceFiles: ts.SourceFile[] = [];

  classMap.forEach((classes, className) => {
    const [temp, sourceFile] = mergeClasses(classes, classSourceMap.get(className)!);
    
    mergedClasses.push(temp);
    mergedSourceFiles.push(sourceFile);
  });


  const printer = ts.createPrinter();
//   const resultFile = ts.createSourceFile(outputFile, '', ts.ScriptTarget.Latest, false, ts.ScriptKind.TS);

  const resultStatements = mergedSourceFiles.map(cls => printer.printNode(ts.EmitHint.Unspecified, cls, cls));
  
  const resultContent = resultStatements.join('\n');

  fs.writeFileSync(outputFile, resultContent, 'utf8');
  
}
if (require.main == module) {
// 示例文件路径
const filePaths = [
    path.join(__dirname, 'file1.ts'),
    path.join(__dirname, 'file2.ts'),
    path.join(__dirname, 'file3.ts') // 添加更多文件路径
  ];
  const outputFile = path.join(__dirname, 'mergedFile.ts');
  
  mergeSourceFiles(filePaths, outputFile);
}
