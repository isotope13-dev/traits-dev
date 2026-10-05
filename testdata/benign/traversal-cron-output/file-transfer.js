export async function transfer(fileService, session) {
    await fileService.uploadFileToServerFileSystem(session, 'report.txt', Buffer.from('report'));
    return fileService.downloadRawFile(session, 'report.txt');
}
