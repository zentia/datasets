import path from "path";
import { readSourceFile } from "./mergeClasses";
import { deleteLogFile, logMessage } from "./log";
import ts from "typescript";

if (require.main == module) {
  deleteLogFile();
  const file = path.join(__dirname, 'file1.ts');
  const sourceFile = readSourceFile(file);
  sourceFile.forEachChild(node=>{
    logMessage(`${ts.SyntaxKind[node.kind]}`);
  });
}