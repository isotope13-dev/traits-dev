<cfscript>
plain = Decrypt(settings[i]["password"], application.key, "AES", "Base64");
</cfscript>
