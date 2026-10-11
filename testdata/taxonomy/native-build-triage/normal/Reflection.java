import java.lang.reflect.Method;
class Reflection { void run(Object target) { Method method = target.getClass().getMethod("main"); method.invoke(target); } }
