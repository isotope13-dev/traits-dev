<cfset u=getPageContext().getRequest().getRequestURL()>
<cfset u="fixed">
<cfset a=encrypt(u,"key","AES")>
