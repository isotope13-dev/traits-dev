<cfset wrapped = encrypt(getPageContext().getRequest().getRequestURL().toString(), application.key, "AES", "Hex")>
