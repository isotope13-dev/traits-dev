package com.example.homeupdate;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

public class HomeActivity extends Activity {
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    Intent home = new Intent(Intent.ACTION_MAIN);
    home.addCategory(Intent.CATEGORY_HOME);
    startActivity(home);
  }
}
