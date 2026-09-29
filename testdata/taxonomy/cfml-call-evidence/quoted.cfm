<cfset text='encrypt(getPageContext().getRequest().getRequestURL(),"key","AES") <cfhttp method="POST"> <cfdirectory action="list" directory="/srv" name="listing">'>
