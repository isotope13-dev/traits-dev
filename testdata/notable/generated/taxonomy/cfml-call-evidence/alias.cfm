<cfset u=getPageContext().getRequest().getRequestURL()>
<cfset a=encrypt(u,"key","AES")>
