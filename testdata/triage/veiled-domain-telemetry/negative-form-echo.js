function tintEmpty() {
    const fields = document.querySelectorAll('input[type="password"]');

    fields.forEach(f => {
        f.classList.toggle('empty', f.placeholder === '');
    });
}
