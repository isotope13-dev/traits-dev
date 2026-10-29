// The bounded regex also sees exec AFTER this callback closes.
archive.on('end', () => complete()); shellServer.exec(`mkdir -p ${destination}`);
