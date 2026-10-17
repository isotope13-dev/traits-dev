package net.fabric;

// Benign naming/control fixture. The environment read and String.equals are
// unrelated to activation; the long literal is an ordinary application label.
public class Demo {
    public static void main(String[] args) {
        String directory = System.getenv("LOCALAPPDATA");
        System.out.println("ExampleApplicationLabel123".equals(directory));
    }
}
