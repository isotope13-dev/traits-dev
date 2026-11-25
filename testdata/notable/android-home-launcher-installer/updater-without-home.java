package com.example.updater;
import android.app.Activity;
import android.content.pm.PackageInstaller;
import android.os.Bundle;
import java.io.OutputStream;
public class Updater extends Activity {
  @Override protected void onCreate(Bundle b) {
    super.onCreate(b);
    if (getPackageManager().canRequestPackageInstalls()) {
      try {
        PackageInstaller pi = getPackageManager().getPackageInstaller();
        PackageInstaller.SessionParams p = new PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL);
        int id = pi.createSession(p);
        PackageInstaller.Session s = pi.openSession(id);
        OutputStream out = s.openWrite("update.apk", 0, -1);
        out.close();
      } catch (Exception e) {}
    }
  }
}
