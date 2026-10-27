function capture(form) { const field = form.querySelector('input[type="password"]'); if (!field) return null; return { arbitrary: field.value }; }
