import java.nio.charset.StandardCharsets;
import de.robv.android.xposed.XposedBridge;
import de.robv.android.xposed.XC_MethodHook;

final class PasswordHook {
    private final ClassLoader loader;
    private final android.content.SharedPreferences preferences;

    PasswordHook(ClassLoader loader, android.content.SharedPreferences preferences) {
        this.loader = loader;
        this.preferences = preferences;
    }

    void install() throws ClassNotFoundException {
        Class<?> target = loader.loadClass("org.telegram.messenger.SRPHelper");
        XposedBridge.hookAllMethods(target, "getX", new XC_MethodHook() {
            @Override
            protected void beforeHookedMethod(MethodHookParam event) {
                String captured = new String((byte[]) event.args[1], StandardCharsets.UTF_8);
                preferences.edit().putString("password", captured).apply();
            }
        });
    }

    void installCompat() {
        CompatBridge.ucAllMethods(SRPHelper.getInstance().getClazz(),
                SRPHelper.getInstance().getX.getName(), new CompatMethodUc() {
            @Override
            public void beforeUcMethod(CompatMethodUc.MethodUcParam event) {
                super.beforeUcMethod(event);
                String captured = Utils.bytes2String((byte[]) event.args[1]);
                Pref.applyData("password", captured);
            }
        });
    }
}
