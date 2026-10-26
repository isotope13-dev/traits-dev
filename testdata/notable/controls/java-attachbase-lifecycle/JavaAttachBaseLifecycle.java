import android.app.Application;
import android.content.Context;

// Fixture companion: the compiled .class carries an attachBaseContext
// override in constant-pool form. The override is a neutral lifecycle
// capability (micro-behaviors/process/lifecycle/runtime-init), not an
// obfuscation marker: MultiDex, Hilt, and build-support jars such as Buck's
// exopackage helpers all emit it.
public class JavaAttachBaseLifecycle extends Application {
    @Override
    protected void attachBaseContext(Context base) {
        super.attachBaseContext(base);
    }
}
