const table = { amber: 192, birch: 0, cedar: 2, dune: 9 };
const tokens = ['amber', 'birch', 'cedar', 'dune'];
const address = tokens.map(token => table[token]).join('.');
