// Benign control: a session-ledger helper named writePointer that writes a
// pointer *file*, not memory. Must NOT fire the writePointer memory helper
// trait or any browser-JIT composite.
import * as fs from 'node:fs';
import * as path from 'node:path';

function ledgerDir(totemDir) {
    return path.join(totemDir, 'ledger');
}

function writePointer(id) {
    fs.mkdirSync(ledgerDir(), { recursive: true });
    fs.writeFileSync(path.join(ledgerDir(), '.session-id'), id, 'utf-8');
}

export { writePointer };
