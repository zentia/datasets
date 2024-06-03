package com.zentiali

import java.io.File
import java.nio.file.Files
import java.nio.file.Paths
import java.nio.file.StandardCopyOption

fun deleteDirectoryContents(directory: File) {
    if (directory.exists() && directory.isDirectory) {
        directory.listFiles()?.forEach { file ->
            if (file.isDirectory) {
                deleteDirectoryContents(file)
            }
            file.delete()
        }
    }
}

fun getRelationPathWithoutExtension(file: File, len:Int): String {
    val nameWithoutExtension = file.nameWithoutExtension
    val parentPath = file.parent
    val pathWithoutExtension = if (parentPath != null) {
        "$parentPath/$nameWithoutExtension"
    } else {
        nameWithoutExtension
    }
    return pathWithoutExtension.substring(len+1)
}

fun getRelationPath(path:String): String {
    return path.substring(srcDirectoryLen+1)
}

fun copyFile(srcPath:String, targetPath:String) {
    val src = Paths.get(srcPath)
    val targetFile = File(targetPath)
    val targetDirectory = File(targetFile.parent)
    if (!targetDirectory.exists()) {
        targetDirectory.mkdirs()
    }
    val target = Paths.get(targetPath)
    Files.copy(src, target, StandardCopyOption.REPLACE_EXISTING)
}