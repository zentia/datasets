package com.zentiali
import java.io.File

const val srcDirectory = "F:\\trunk_proj\\Project\\RawAssets\\LuaScripts\\Logic\\UISystem"
const val srcDirectoryLen = srcDirectory.length
var targetDirectory = "G:\\OSCE_0704\\Project\\DevAssets\\TypeScript\\src\\system\\ui-system"
const val outputDirectory = "D:/datasets/output/lua"
const val outputTsDirectory = "D:\\datasets\\output\\typescript"
const val outputTsDirectoryLen = outputTsDirectory.length

fun getTypescriptPath(file: File, len: Int): File {
    var relationPath = getRelationPathWithoutExtension(file, len)
    relationPath = "$relationPath.mts"
    var tsPath = camelToKebabCase(relationPath)
    tsPath = "$targetDirectory\\$tsPath"
    val tsFile = File(tsPath)
    return tsFile
}

fun extractFile(directory: File, client: Client) {
    if (directory.exists() && directory.isDirectory) {
        for (file in directory.listFiles()!!) {
            if (file.isDirectory) {
                extractFile(file, client)
            } else {
                if (file.path.endsWith("_AutoBind.lua")) {
                    continue
                }
                val tsFile = getTypescriptPath(file, srcDirectoryLen)
                if (tsFile.exists()) {
                    continue
                }
                println(tsFile.path)
                client.input(file.path)
            }
        }
    }
}

fun findMissingFiles() {
    val c = Client()
    c.introduce()
    val outputFile = File(outputDirectory)
    deleteDirectoryContents(outputFile)
    val srcDirectoryFile = File(srcDirectory)
    extractFile(srcDirectoryFile, c)
}

fun splitFile(filePath: String) {
    val file = File(filePath)
    if (file.exists() && file.isFile) {
        val c = Client()
        c.introduce()
        c.input(filePath)
    }
}

fun outputTypeScript(directory: File) {
    if (directory.exists() && directory.isDirectory) {
        for (file in directory.listFiles()!!) {
            if (file.isDirectory) {
                outputTypeScript(file)
            } else {
                if (file.nameWithoutExtension.contains('@')) {
                    continue
                }
                val tsFile = getTypescriptPath(file, outputTsDirectoryLen)
                if (tsFile.exists()) {
                    continue
                }
                println(tsFile.path)
                copyFile(file.path,tsFile.path)
            }
        }
    }
}

fun camelToKebabCase(input: String): String {
    var result = input.replace(Regex("([a-z])([A-Z])"), "$1-$2")
            .replace(Regex("([A-Z])([A-Z][a-z])"), "$1-$2")
            .lowercase()
    if (result.endsWith("init.mts")) {
        result = result.replace("init.mts", "index.mts");
    }
    return result.replace("_","-");
}

fun main(args: Array<String>) {
    if (args.size == 1) {
        val filePath = args[0]
        splitFile(filePath)
    } else if (args.size == 2) {
        val kind = args[0]
        targetDirectory = args[1];
        if (kind == "lua") {
            findMissingFiles()
        } else if (kind == "ts") {
            val targetFile = File(outputTsDirectory)
            outputTypeScript(targetFile)
        }
    }
}