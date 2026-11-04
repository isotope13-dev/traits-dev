import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL

// Positive control for the JVM download-to-disk capability: Kotlin fetches a
// remote file into a cache path with renamed identifiers and property-style
// stream access. Neither execution of the fetched file nor its purpose is
// claimed; this is the ordinary-updater shape the notable capability covers.
class KotlinDownloadVariant(private val cache: File) {
    fun pull(link: String, name: String): File {
        val target = File(cache, name)
        val c = URL(link).openConnection() as HttpURLConnection
        try {
            val src = c.inputStream
            val dst = FileOutputStream(target)
            val buf = ByteArray(4096)
            while (true) {
                val n = src.read(buf)
                if (n <= 0) break
                dst.write(buf, 0, n)
            }
            dst.close()
        } finally {
            c.disconnect()
        }
        return target
    }
}
