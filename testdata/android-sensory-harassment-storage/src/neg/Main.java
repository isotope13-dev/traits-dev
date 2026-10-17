public class Main {
    public void flash(android.hardware.camera2.CameraManager cm) throws Exception {
        cm.setTorchMode("0", true);
        java.io.File dir = android.os.Environment.getExternalStorageDirectory();
        if (dir == null) throw new Exception("no storage");
    }
}
