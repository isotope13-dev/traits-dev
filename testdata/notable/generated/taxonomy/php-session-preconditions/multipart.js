const body = 'Content-Disposition: form-data; name="file"; filename="image.png"\r\n' +
    'Content-Type: image/png\r\n\r\nimage';
fetch('https://example.invalid/upload', {method: 'POST', body});
