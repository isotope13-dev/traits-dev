// import(filename);
const help = 'import(filename);';
const adapter = { import(filename) { return filename; } };
adapter.import(filename);
import('./literal.js', options);
