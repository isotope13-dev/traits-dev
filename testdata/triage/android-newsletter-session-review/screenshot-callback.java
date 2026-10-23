import android.accessibilityservice.AccessibilityService;
class ScreenCapture extends AccessibilityService {
 void capture() { takeScreenshot(0, executor, callback); }
 void onAccessibilityEvent(android.view.accessibility.AccessibilityEvent event) { }
 void onInterrupt() { }
}
