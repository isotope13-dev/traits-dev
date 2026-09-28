import java.io.File;
import java.lang.reflect.Method;
import java.net.URLClassLoader;

final class JavaLocalUrlClassLoader {
    static void invoke(File localJar, String className) throws Exception {
        try (URLClassLoader loader = new URLClassLoader(
                new java.net.URL[] { localJar.toURI().toURL() }, null)) {
            Class<?> mainClass = loader.loadClass(className);
            Method main = mainClass.getMethod("main", String[].class);
            main.invoke(null, (Object) new String[0]);
        }
    }
}
