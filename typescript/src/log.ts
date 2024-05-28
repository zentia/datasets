import * as fs from 'fs';
import * as path from 'path';

const logFilePath = path.join(__dirname, 'app.log');

export function logMessage(messages: string): void {
    fs.appendFile(logFilePath,`${messages}\n`, (err) => {
        if (err) {
            console.error(`Failed to write to log file: ${err.message}`);
        }
    });
}