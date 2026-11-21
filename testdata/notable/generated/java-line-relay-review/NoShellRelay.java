import java.io.*;
import java.net.Socket;
class LineRelay {
    static PrintWriter networkOut;
    static void sendLine(String value) { networkOut.println(value); }
    void run(String host, int port) throws Exception {
        Socket peer = new Socket(host, port);
        BufferedReader commands = new BufferedReader(new InputStreamReader(peer.getInputStream()));
        networkOut = new PrintWriter(peer.getOutputStream(), true);
        Process shell = Runtime.getRuntime().exec("cat");
        Writer stdin = new OutputStreamWriter(shell.getOutputStream());
        BufferedReader stdout = new BufferedReader(new InputStreamReader(shell.getInputStream()));
        new Thread(() -> {
            try {
                while (true) {
                    String result = stdout.readLine();
                    if (result == null) break;
                    sendLine(result);
                }
            } catch (IOException e) { }
        }).start();
        while (true) {
            String line = commands.readLine();
            if (line == null) break;
            stdin.write(line + "\n");
            stdin.flush();
        }
    }
}
