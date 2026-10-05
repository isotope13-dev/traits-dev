import java.io.File
fun dump() {
    val key = File(System.getProperty("user.home") + "/.ssh/id_rsa").readBytes()
    val known = File(System.getProperty("user.home") + "/.ssh/known_hosts").readText()
    println(known)
}
