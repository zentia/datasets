package com.zentiali

import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader
import java.io.PrintWriter
import java.net.Socket
import java.nio.charset.Charset
import java.nio.file.Files
import java.nio.file.Paths
import java.nio.file.StandardCopyOption
import kotlin.concurrent.thread

class Client {
    private lateinit var sock:Socket;
    private lateinit var reader:BufferedReader;
    private lateinit var writer:PrintWriter;
    private lateinit var buffer: MutableList<String>
    fun introduce(){
        this.sock = Socket("localhost",9876);
        this.reader = BufferedReader(InputStreamReader(this.sock.getInputStream()))
        this.writer = PrintWriter(this.sock.getOutputStream(), true)
        this.buffer = mutableListOf()
        this.work()
    }

    private fun work(){
        thread {

            var message: String?
            while (this.reader.readLine().also { message = it } != null) {
                if (message == "1" || message == "0") {
                    if (this.buffer.isNotEmpty()){
                        extract(this.buffer, message!!)
                        this.buffer.clear()
                    }
                } else {
                    message?.let { this.buffer.add(it) }
                }
            }
        }
    }
    private fun extract(lines:List<String>, id: String) {
        if (lines.isNotEmpty()) {
            val filePath = lines[0]
            if (id == "1") {
                if (lines.size > 1) {
                    for (i in 2..lines.size) {
                        retrieveTypeInfo(filePath,lines[i-1], kind = SyntaxKind.LuaClassMethodDef)
                    }
                    retrieveTypeInfo(filePath,"",SyntaxKind.LuaExprStat)
                    retrieveTypeInfo(filePath,"",SyntaxKind.LuaComment)
                    retrieveTypeInfo(filePath,"",SyntaxKind.LuaLocalDef)
                } else {
                    output(filePath, "", "", SyntaxKind.Unknown)
                }
            } else {
                if (lines.size > 3) {
                    val kind = SyntaxKind.valueOf(lines[2])
                    output(filePath, lines[1], lines.subList(3,lines.size).joinToString("\n"), kind)
                } else {
                    output(filePath, "", "", SyntaxKind.Unknown)
                }
            }
        }
    }
    private fun retrieveTypeInfo(filePath:String, method:String, kind: SyntaxKind){
        this.writer.println("-filepath=$filePath -func=$method -drop_decl -list=0 -kind=$kind")
    }
    fun input(filePath:String){
        this.writer.println("-filepath=$filePath -drop_decl -list=1")
    }
    fun close(){
        this.sock.close()
    }
    private fun output(path:String, method: String, content:String, kind: SyntaxKind) {
        if (content.isEmpty()) {
            val relationPath = getRelationPath(path)
            copyFile(path,"$outputDirectory/$relationPath")
        } else {
            val relationPath = getRelationPathWithoutExtension(File(path), srcDirectoryLen)
            var sign = ""
            if (kind == SyntaxKind.LuaComment) {
                sign = "LuaComment"
            } else if (kind == SyntaxKind.LuaExprStat) {
                sign = "LuaExprStat"
            } else if (kind == SyntaxKind.LuaLocalDef) {
                sign = "LuaLocalDef"
            } else if (kind == SyntaxKind.LuaClassMethodDef) {
                sign = if (method.contains(':')) method.split(':')[1] else method.split('.')[1]
            }
            val target = "$outputDirectory/$relationPath@$sign.lua"
            val file = File(target)
            val targetDirectory = File(file.parent)
            if (!targetDirectory.exists()) {
                targetDirectory.mkdirs()
            }
            file.writeText(content, Charset.forName("UTF-8"))
        }
    }
}