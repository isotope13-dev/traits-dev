public class JavaPlatformLifecycle {
    public static void main(String[] args) {
        String os = System.getProperty("os.name");
        String user = System.getProperty("user.name");
        Runtime.getRuntime().addShutdownHook(new Thread(() ->
            System.out.println("completed on " + os + " for " + user)));
        byte[] buffer = new byte[1_048_576];
        System.out.println(buffer.length);
    }
}
