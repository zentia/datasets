import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.PrintStream

import java.net.Socket

fun main(args: Array<String>) {
    val client = Socket("localhost", 9876)

    val output = PrintStream(client.getOutputStream())

    val input = BufferedReader(InputStreamReader(client.getInputStream()))

    var str = ""
    for (arg in args) {
        str += arg
        str += " "
    }
    output.println(str)
    println("Server response:")
    while (true) {
        val response = input.readLine() ?: break
        println(response)
    }
    client.close()
}