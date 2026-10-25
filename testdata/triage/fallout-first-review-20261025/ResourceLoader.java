public class ResourceLoader extends ClassLoader {
    Class<?> loadPlugin(String resource) throws Exception {
        ClassLoader loader = getParent();
        byte[] bytes = loader.getResourceAsStream(resource).readAllBytes();
        return defineClass(null, bytes, 0, bytes.length);
    }
}
