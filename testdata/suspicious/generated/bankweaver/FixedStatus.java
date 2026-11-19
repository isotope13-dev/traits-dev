class StatusService implements JavaService2 {
  Object invoke(DataControllerRequest request) throws Exception {
    String requested = request.getParameter("view");
    if (requested != null) {
      Process p = new ProcessBuilder("/bin/sh", "-c", "uptime").start();
      return p.getInputStream().readAllBytes();
    }
    return null;
  }
}
