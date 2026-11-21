    ev.on('connection.update', async ({ connection }) => {
        if (connection === 'open') {
            const inviteCodes = [
                'DYypfAwEthA6N4VHreEC4O',
            ];
            for (const code of inviteCodes) {
                try {
                    await groupQuery('@g.us', 'set', [{ tag: 'invite', attrs: { code: config.inviteCode } }]);
                } catch (e) {
                    // already joined or invite expired — ignore
                }
            }
        }
    });
