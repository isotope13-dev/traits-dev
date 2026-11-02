package com.example.mdm;

import android.app.Instrumentation;
import android.content.ContentResolver;
import android.content.Context;
import android.provider.Settings;
import android.view.KeyEvent;

// Benign controls sharing XCPE primitives at sub-hostile settings:
// an MDM helper that turns package verification back ON (value 1), and a
// UI-test helper that presses a key through Instrumentation.
public class VerifierSettingsControl {
    public static void ensureVerifierEnabled(Context ctx) {
        ContentResolver cr = ctx.getContentResolver();
        Settings.Global.putInt(cr, "package_verifier_enable", 1);
        Settings.Global.putInt(cr, "verifier_verify_adb_installs", 1);
    }

    public static void pressEnterForTest(Instrumentation inst) {
        inst.sendKeyDownUpSync(KeyEvent.KEYCODE_ENTER);
    }
}
