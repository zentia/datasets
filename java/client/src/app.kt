package com.zentiali
import java.io.File

const val srcDirectory = "F:\\trunk_proj\\Project\\RawAssets\\LuaScripts\\Logic\\UISystem"
const val srcDirectoryLen = srcDirectory.length
const val targetDirectory = "G:\\OSCE_0704\\Project\\DevAssets\\TypeScript\\src\\system\\ui-system"
const val outputDirectory = "D:/datasets/output/lua"

fun extractFile(directory: File, client: Client) {
    if (directory.exists() && directory.isDirectory) {
        directory.listFiles()?.forEach { file ->
            if (file.isDirectory) {
                extractFile(file, client)
            } else {
                if (file.path.endsWith("_AutoBind.lua")) {
                    return
                }
                var relationPath = getRelationPathWithoutExtension(file)
                relationPath = "$relationPath.mts"
                var tsPath = camelToKebabCase(relationPath)
                tsPath = "$targetDirectory\\$tsPath"
                val tsFile = File(tsPath)
                if (tsFile.exists()) {
                    return
                }
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

fun camelToKebabCase(input: String): String {
    return input.replace(Regex("([a-z])([A-Z])"), "$1-$2")
            .replace(Regex("([A-Z])([A-Z][a-z])"), "$1-$2")
            .lowercase()
}

fun main(args: Array<String>) {
    findMissingFiles()
}