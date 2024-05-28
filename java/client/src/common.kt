package com.zentiali

import java.io.File

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

fun getRelationPathWithoutExtension(file: File): String {
    val nameWithoutExtension = file.nameWithoutExtension
    val parentPath = file.parent
    val pathWithoutExtension = if (parentPath != null) {
        "$parentPath/$nameWithoutExtension"
    } else {
        nameWithoutExtension
    }
    return pathWithoutExtension.substring(srcDirectoryLen+1)
}

fun getRelationPath(path:String): String {
    return path.substring(srcDirectoryLen+1)
}