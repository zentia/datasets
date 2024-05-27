import { readFileSync } from "fs";
import * as ts from "typescript";


// const filename = "test.ts";
// const code = `const test: number = 1 + 2;`;

// const sourceFile = ts.createSourceFile(
//     filename, code, ts.ScriptTarget.Latest
// );

function printRecursiveFrom(
    node: ts.Node, indentLevel: number, sourceFile: ts.SourceFile
) {
    const indentation = "-".repeat(indentLevel);
    if (node.kind != ts.SyntaxKind.SourceFile) {
        const syntaxKind = ts.SyntaxKind[node.kind];
        const nodeText = node.getText(sourceFile);
        console.log(`${indentation}${syntaxKind}: ${nodeText}`);
    }
    

    node.forEachChild(child =>
        printRecursiveFrom(child, indentLevel + 1, sourceFile)
    );
}

// printRecursiveFrom(sourceFile, 0, sourceFile);

// export function delint(sourceFile: ts.SourceFile) {
//     delintNode(sourceFile);

//     function delintNode(node: ts.Node) {
//         // switch (node.kind) {
//         //     case ts.SyntaxKind.SourceFile:
//         //         ts.forEachChild(node, delintNode);
//         //         return;
//         // }
//         const syntaxKind = ts.SyntaxKind[node.kind];
//         console.log(node.kind);
//         if (ts.isClassDeclaration(node)){
//             console.log(node.name);
//         }
        
//         ts.forEachChild(node, delintNode);
//     }
// }



export function testAst(){
    const fileNames = process.argv.slice(2);
    fileNames.forEach(fileName => {
        // Parse a file
        const sourceFile = ts.createSourceFile(fileName,readFileSync(fileName).toString(), ts.ScriptTarget.ES2015);
        // delint(sourceFile);
        printRecursiveFrom(sourceFile,0,sourceFile);
    });
}