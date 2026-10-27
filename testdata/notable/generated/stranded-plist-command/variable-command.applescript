set commandText to "echo ready"
set job to "<key>ProgramArguments</key>" & return & "<array>" & return & "<string>/bin/bash</string>" & return & "<string>-c</string>" & return & "<string>" & commandText & "</string>" & return & "</array>"
