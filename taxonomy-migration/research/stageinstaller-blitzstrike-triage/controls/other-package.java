import android.content.Context;
import android.content.IntentSender;
import android.content.pm.PackageInstaller;
import java.io.InputStream;
import java.io.OutputStream;

class StageInstaller {
    void install(Context context, InputStream apk, IntentSender callback) throws Exception {
        new ProcessBuilder("sh", "-c", "pm disable com.example.optional").start().waitFor();
        PackageInstaller pi = context.getPackageManager().getPackageInstaller();
        PackageInstaller.SessionParams params = new PackageInstaller.SessionParams(
            PackageInstaller.SessionParams.MODE_FULL_INSTALL);
        int id = pi.createSession(params);
        PackageInstaller.Session session = pi.openSession(id);
        try (OutputStream out = session.openWrite("base.apk", 0, -1)) {
            byte[] buffer = new byte[8192];
            int count;
            while ((count = apk.read(buffer)) != -1) out.write(buffer, 0, count);
            session.fsync(out);
        }
        session.commit(callback);
    }
    void onInstallResult() throws Exception {
        new ProcessBuilder("sh", "-c", "pm enable com.example.optional").start().waitFor();
    }
}
