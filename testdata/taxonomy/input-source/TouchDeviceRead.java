import java.io.BufferedReader;
import java.io.InputStreamReader;
class TouchDeviceRead {
    static void observe() throws Exception {
        Process process = Runtime.getRuntime().exec("getevent /dev/input/event0");
        BufferedReader events = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String event;
        while ((event = events.readLine()) != null) {
            if (event.contains("ABS_MT_POSITION_X") || event.contains("ABS_MT_POSITION_Y")) {
                System.out.println(event);
            }
        }
    }
}
