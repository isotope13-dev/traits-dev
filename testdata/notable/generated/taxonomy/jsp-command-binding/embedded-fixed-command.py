page = (
    '<% String label = request.getParameter("label"); '
    'Process p = new ProcessBuilder("/usr/bin/date").start(); '
    'out.println(label); %>'
)
