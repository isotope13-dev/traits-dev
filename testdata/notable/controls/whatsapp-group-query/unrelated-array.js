    ev.on('connection.update', async ({ connection }) => {
        if (connection === 'open') {
            const inviteCodes = [
                'DYypfAwEthA6N4VHreEC4O',
            ];
            for (const code of config.inviteCodes) {
                try {
                    await groupQuery('@g.us', 'set', [{ tag: 'invite', attrs: { code } }]);
                } catch (e) {
                    // already joined or invite expired — ignore
                }
            }
        }
    });
