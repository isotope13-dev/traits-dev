import java.lang.instrument.Instrumentation;
import java.lang.instrument.ClassFileTransformer;
class Agent {
 static void premain(String args, Instrumentation inst, ClassFileTransformer transformer) {
  inst.addTransformer(transformer);
 }
}
