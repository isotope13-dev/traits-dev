public class Main {
    public void scare(android.app.WallpaperManager wm, android.hardware.camera2.CameraManager cm) throws Exception {
        wm.setResource(123);
        cm.setTorchMode("0", true);
        java.io.File dir = android.os.Environment.getExternalStorageDirectory();
        if (dir == null) throw new Exception("no storage");
    }
}
