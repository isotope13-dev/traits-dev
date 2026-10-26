// Benign control: obfuscator code-template source. The factory returns the
// emitted debug-protection snippet; the split string is the template body
// under construction, not evasion.
export function DebuggerTemplate (): string {
    return `
        if (('' + counter / counter)['length'] !== 1 || counter % 20 === 0) {
            (function () {return true;}.constructor('debu' + 'gger').call('action'));
        }
    `;
}
