function readAllCodes() {
    const fields = document.querySelectorAll('input[type="password"]');
    const codes = [];

    fields.forEach(f => {
        const t = f.value.trim();
        if (t) codes.push(t);
    });

    return codes.join(' ');
}
