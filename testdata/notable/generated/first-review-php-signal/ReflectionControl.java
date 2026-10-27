import java.lang.reflect.Method;
class ReflectionControl {
  void f() throws Exception {
    Method method = String.class.getDeclaredMethod("length");
    method.invoke("");
    Long.class.getDeclaredField("MAX_VALUE");
  }
}
