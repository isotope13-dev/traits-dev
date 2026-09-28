import java.applet.Applet;

final class JavaAppletParameter {
    static String read(Applet applet) {
        return applet.getParameter("orb-class");
    }
}
