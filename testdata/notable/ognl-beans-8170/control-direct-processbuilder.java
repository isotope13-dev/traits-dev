public class ListFiles {
    public static void run() throws Exception {
        new ProcessBuilder("/bin/sh", "-c", "ls").start();
    }
}
