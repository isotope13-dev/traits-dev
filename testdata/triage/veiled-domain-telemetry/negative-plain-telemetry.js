const ENDPOINT = 'https://telemetry.example.com/collect.php';


async function reportUsage(evt) {
    if (!evt || typeof evt !== 'object') return;

    try {
        const payload = {
            app: 'Demo',
            at: Date.now(),
            ver: '2.0',
            ...evt
        };

        const response = await fetch(ENDPOINT, {
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
