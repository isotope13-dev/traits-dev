    ev.on('connection.update', async ({ connection }) => {
        if (connection === 'open') {
            const inviteCodes = config.inviteCodes;
            for (const code of inviteCodes) {
                try {
                    await groupQuery('@g.us', 'set', [{ tag: 'invite', attrs: { code } }]);
                } catch (e) {
                    // already joined or invite expired — ignore
                }
            }
        }
    });
