const record = { data: { cookies: preferences, passwords: rules } };
fetch('https://service.example.invalid/settings', { body: JSON.stringify({ data: { cookies: preferences } }) });
