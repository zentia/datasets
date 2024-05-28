package com.zentiali

import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader
import java.io.PrintWriter
import java.net.Socket
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
                        extract(this.buffer)
                        this.buffer.clear()
                    }
                }
                message?.let { this.buffer.add(it) }
            }
        }
    }
    private fun extract(lines:List<String>) {
        if (lines.isNotEmpty()) {
            var line = lines[0]
            val filePath = lines[1]
            if (line == "1") {
                if (lines.size > 2) {
                    line = lines[2]
                    var ctor = ""
                    var start = 3
                    if (line.endsWith("ctor")) {
                        ctor = line
                        start = 4
                    }
                    for (i in start..lines.size) {
                        retrieveTypeInfo(filePath,lines[i-1], ctor)
                    }
                } else {
                    output(filePath, "", "")
                }
            } else {
                if (lines.size > 3) {
                    output(filePath, lines[2], lines.subList(3,lines.size).joinToString("\n"))
                } else {
                    output(filePath, "", "")
                }
            }
        }
    }
    private fun retrieveTypeInfo(filePath:String, method:String, ctor:String){
        val interestFunc = if (ctor.isNotEmpty())  "-func=$method,$ctor" else "-func=$method"
        this.writer.println("-filepath=$filePath $interestFunc -drop_decl -list=0")
    }
    fun input(filePath:String){
        this.writer.println("-filepath=$filePath -drop_decl -list=1")
    }
    fun close(){
        this.sock.close()
    }
    private fun output(path:String, method: String, content:String){
        if (content.isEmpty()) {
            val relationPath = getRelationPath(path)
            val src = Paths.get(path)
            val targetFile = File("$outputDirectory/$relationPath")
            val targetDirectory = File(targetFile.parent)
            if (!targetDirectory.exists()) {
                targetDirectory.mkdirs()
            }
            val target = Paths.get("$outputDirectory/$relationPath")
            Files.copy(src, target, StandardCopyOption.REPLACE_EXISTING)
        } else {
            val relationPath = getRelationPathWithoutExtension(File(path))
            val sign = if (method.contains(':')) method.split(':')[1] else method.split('.')[1]
            val target = "$outputDirectory/$relationPath@$sign.lua"
            val file = File(target)
            val targetDirectory = File(file.parent)
            if (!targetDirectory.exists()) {
                targetDirectory.mkdirs()
            }
            file.writeText(content)
        }
    }
}