function render(value, table, parse) { const key=value.substring(0, 11); const entry=table[key]; return entry("x", parse(value)); }
