import java.net.URLClassLoader;
import java.lang.reflect.Method;
class Loading { void run(URLClassLoader loader) { Method method = loader.getClass().getMethod("main"); method.invoke(loader); } }
