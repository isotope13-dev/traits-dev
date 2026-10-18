class FileOutput { void save(byte[] data) throws Exception { FileOutputStream f = new FileOutputStream("output"); f.write(data); } }
