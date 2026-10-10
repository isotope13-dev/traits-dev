function send(response, value) { response.json(value); response.status(200).json({ok: true}); }
