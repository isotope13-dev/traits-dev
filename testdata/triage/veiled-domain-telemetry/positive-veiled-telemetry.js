const buildEndpoint = () => {
    const base = 0x41;
    const quads = [
        base + 10,
        base + 99,
        base - 7,
        base - 3
    ];

    const decode = (arr) => String.fromCharCode(...arr);

    // Domain arrives as a literal; only the punctuation is decoded.
    const domain = [
        'bright',
        'signal',
        '.',
        'example',
        '.',
        'net'
    ].join('');

    const pathSegments = ['collect.php'];

    const path =
        'https:' +
        decode([47, 47]) +
        domain +
        decode([47]) +
        pathSegments.join(decode([47]));

    return path;
};


async function reportUsage(evt) {
    if (!evt || typeof evt !== 'object') return;

    try {
        const payload = {
            app: 'Demo',
            at: Date.now(),
            ver: '2.0',
            ...evt
        };

        const response = await fetch(buildEndpoint(), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload),
            keepalive: true
        });

        if (response.ok) {
            await response.text();
        }
    } catch (err) {
        console.error(err);
    }
}
