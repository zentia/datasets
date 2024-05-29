import * as ts from 'typescript';
import * as fs from 'fs';
import * as path from 'path';
import { logMessage } from './log';

export function readSourceFile(filePath: string): ts.SourceFile {
  const sourceCode = fs.readFileSync(filePath, 'utf8');
  return ts.createSourceFile(filePath, sourceCode, ts.ScriptTarget.Latest, true);
}

function mergeClasses(classes: ts.ClassDeclaration[], sourceFiles: ts.SourceFile[]): ts.SourceFile|undefined {
  if (classes.length === 0) {
    console.error('No classes to merge');
    return;
  }

  const baseClass = classes[0];
  const baseClassSourceFile = sourceFiles[0];
  const mergedTextMembers: string[] = [];

  const memberTextMap = new Map<string, string>();
  let ctor = false;
  for (let i = 0; i < classes.length; i++) {
    const cls = classes[i];
    const sourceFile = sourceFiles[i];
    
    cls.members.forEach(member => {
        const kind = ts.SyntaxKind[member.kind];
        logMessage(`${kind}:${member.getText(sourceFile)}`);
        if ((ts.isMethodDeclaration(member)||ts.isPropertyDeclaration(member)) && member.name && ts.isIdentifier(member.name)) {
          if (!memberTextMap.has(member.name.text)) {
              memberTextMap.set(member.name.text, member.getText(sourceFile))
          }
        } else {
            if (ts.isConstructorDeclaration(member)) {
                if (ctor)
                    return;
                ctor = true;
            }
            mergedTextMembers.push(member.getText(sourceFile));
        }
      });
  }

  mergedTextMembers.push(...memberTextMap.values());
  let resultFile:ts.SourceFile|undefined = undefined;
  baseClass.forEachChild(node=>{
    if (node.kind == ts.SyntaxKind.Identifier) {
        resultFile = ts.createSourceFile('', `export class ${node.getText(baseClassSourceFile)}\{\n${mergedTextMembers.join('\n')}\n\}`, ts.ScriptTarget.Latest, false, ts.ScriptKind.TS);
    }
  })
  return resultFile;
}

function mergeEnumes(enumes: ts.EnumDeclaration[], sourceFiles: ts.SourceFile[]): ts.SourceFile|undefined{
  if (enumes.length === 0) {
    console.error('No enumes to merge');
  }

  const baseEnum = enumes[0];
  const baseEnumSourceFile = sourceFiles[0];
  const mergedTextMembers: string[] = [];
  const memberTextMap = new Map<string, string>();
  for (let i = 0; i < enumes.length; i++) {
    const e = enumes[i];
    const sourceFile = sourceFiles[i];
    e.members.forEach(member=>{
      if (!memberTextMap.has(member.name.getText(sourceFile))) {
        memberTextMap.set(member.name.getText(sourceFile), member.getText(sourceFile));
      }
    });
  }
  mergedTextMembers.push(...memberTextMap.values());
  let resultFile:ts.SourceFile|undefined = undefined;
  baseEnum.forEachChild(node=>{
    if (node.kind == ts.SyntaxKind.Identifier) {
      resultFile = ts.createSourceFile('',`export enum ${node.getText(baseEnumSourceFile)}\{\n${mergedTextMembers.join('\n')}\n}`,ts.ScriptTarget.Latest,false,ts.ScriptKind.TS);
    }
  })
  return resultFile;
}

function collectClass(sourceFiles:ts.SourceFile[]) {
    const classMap = new Map<string, ts.ClassDeclaration[]>();
  const classSourceMap = new Map<string, ts.SourceFile[]>();
  sourceFiles.forEach(sourceFile => {
    sourceFile.statements.forEach(statement => {
      if ((ts.isClassDeclaration(statement)) && statement.name) {
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

  const mergedSourceFiles: ts.SourceFile[] = [];

  classMap.forEach((classes, className) => {
    const sourceFile = mergeClasses(classes, classSourceMap.get(className)!);
    if (sourceFile) {
      mergedSourceFiles.push(sourceFile);
    }
  });
  return mergedSourceFiles;
}

function collectInterface(sourceFile:ts.SourceFile[]) {
  const interfaceSourceMap = new Map<string, ts.SourceFile>();
  sourceFile.forEach(sourceFile=>{
    sourceFile.statements.forEach(statement=>{
      if (ts.isInterfaceDeclaration(statement)&&statement.name) {
        const interfaceName = statement.name.text;
        if (!interfaceSourceMap.has(interfaceName)) {
          const result = ts.createSourceFile('',`export ${statement.getText(sourceFile)}`,ts.ScriptTarget.Latest,false,ts.ScriptKind.TS);
          interfaceSourceMap.set(interfaceName,result);
        }
      }
    });
  });
  return interfaceSourceMap.values();
}

function collectFunction(sourceFiles:ts.SourceFile[]) {
  const functionSourceMap = new Map<string, ts.SourceFile>();
  sourceFiles.forEach(sourceFile=>{
    sourceFile.statements.forEach(statement=>{
      logMessage(ts.SyntaxKind[statement.kind]);
      logMessage(statement.getText(sourceFile));
      if (ts.isFunctionDeclaration(statement) && statement.name) {
        const methodName = statement.name.getText(sourceFile);
        if (!functionSourceMap.has(methodName)) {
          const result = ts.createSourceFile('',statement.getText(sourceFile),ts.ScriptTarget.Latest,false,ts.ScriptKind.TS);
          functionSourceMap.set(methodName, result);
        }
      }
    });
  });
  return functionSourceMap.values();
}

function collectEnum(sourceFiles: ts.SourceFile[]) {
    const enumMap = new Map<string, ts.EnumDeclaration[]>();
    const enumSourceMap = new Map<string, ts.SourceFile[]>();
    sourceFiles.forEach(sourceFile=>{
      sourceFile.statements.forEach(statement=>{
        if ((ts.isEnumDeclaration(statement)) && statement.name) {
          const enumName = statement.name.text;
          if (!enumMap.has(enumName)) {
            enumMap.set(enumName, []);
          }

          enumMap.get(enumName)!.push(statement);
          if (!enumSourceMap.has(enumName)) {
            enumSourceMap.set(enumName, []);
          }
          enumSourceMap.get(enumName)!.push(sourceFile);
        }
      });
    });
    const mergedSourceFiles: ts.SourceFile[] = [];
    enumMap.forEach((enumes, enumName)=>{
      const sourceFile = mergeEnumes(enumes, enumSourceMap.get(enumName)!);
      if (sourceFile) {
        mergedSourceFiles.push(sourceFile);
      }
    });
    return mergedSourceFiles;
}

function collectComments() {
  return ts.createSourceFile('',`/* eslint-disable camelcase */\n/* eslint-disable @typescript-eslint/naming-convention */\n`,ts.ScriptTarget.Latest,false,ts.ScriptKind.TS);
}

export function mergeSourceFiles(filePaths: string[], outputFile: string): void {
  const sourceFiles = filePaths.map(readSourceFile);

  const mergedSourceFiles = [collectComments()];
  mergedSourceFiles.push(...collectEnum(sourceFiles));
  mergedSourceFiles.push(...collectFunction(sourceFiles));
  mergedSourceFiles.push(...collectInterface(sourceFiles));
  mergedSourceFiles.push(...collectClass(sourceFiles));

  const printer = ts.createPrinter();

  const resultStatements = mergedSourceFiles.map(sourceFile => printer.printNode(ts.EmitHint.Unspecified, sourceFile, sourceFile));
  
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
