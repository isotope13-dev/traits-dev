import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

// Test-suite helper: query the terminal width so progress output can wrap.
// Shelling out for `stty size` is ordinary process execution, not evasion:
// there is no HTTP handler, no request input, and no attacker-controlled
// command construction anywhere near this call.
public class TerminalWidthProbe {
    static int retrieveTerminalWidth() {
        try {
            final ProcessBuilder builder = new ProcessBuilder("/bin/sh", "-c", "stty size </dev/tty");
            final Process process = builder.start();
            final BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            final String output = reader.readLine();
            if (process.waitFor() != 0) {
                return -1;
            }
            return Integer.parseInt(output.split(" ")[1]);
        } catch (IOException | InterruptedException e) {
            return -1;
        }
    }
}
