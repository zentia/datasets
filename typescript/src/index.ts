import { testAst } from "./ast.js";
import * as fs from 'fs';
import * as path from 'path';

const filePath = path.join(__dirname, 'app.log');

try {
    fs.unlinkSync(filePath);
    console.log('File deleted successfully.');
} catch (err) {
    console.error(`Failed to delete file: ${err}`);
}


testAst();