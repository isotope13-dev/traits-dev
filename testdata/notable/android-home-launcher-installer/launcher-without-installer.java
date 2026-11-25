package com.example.launcher;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
public class Launcher extends Activity {
  @Override protected void onCreate(Bundle b) {
    super.onCreate(b);
    Intent home = new Intent(Intent.ACTION_MAIN);
    home.addCategory(Intent.CATEGORY_HOME);
    startActivity(home);
    if (getPackageManager().canRequestPackageInstalls()) { finish(); }
  }
}
