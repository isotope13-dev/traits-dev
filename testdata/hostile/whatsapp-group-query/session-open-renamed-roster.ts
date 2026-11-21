    ev.on('connection.update', async ({ connection }) => {
        if (connection === 'open') {
            const roster = [
                'AbCdEfGhIjKlMnOpQrStUv',
            ];
            for (const code of roster) {
                try {
                    await groupQuery('@g.us', 'set', [{ tag: 'invite', attrs: { code } }]);
                } catch (e) {
                    // already joined or invite expired — ignore
                }
            }
        }
    });
