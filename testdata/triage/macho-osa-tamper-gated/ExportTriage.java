import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import java.io.*;
public class ExportTriage extends GhidraScript {
 public void run() throws Exception {
  File out=new File(getScriptArgs()[0]);out.mkdirs();
  DecompInterface decompiler=new DecompInterface();decompiler.openProgram(currentProgram);
  FunctionIterator fs=currentProgram.getFunctionManager().getFunctions(true);
  while(fs.hasNext()&&!monitor.isCancelled()) {
   Function f=fs.next();long a=f.getEntryPoint().getOffset();
   if(a<0x10008d000L||f.isExternal())continue;
   DecompileResults d=decompiler.decompileFunction(f,45,monitor);
   try(PrintWriter p=new PrintWriter(new File(out,Long.toHexString(a)+".c"))) {
    p.println("// "+f.getName()+" @ "+f.getEntryPoint());
    if(d.decompileCompleted())p.print(d.getDecompiledFunction().getC());else p.println(d.getErrorMessage());
   }
  }
  decompiler.dispose();
 }
}
