#!/usr/bin/env python3
"""Static regression checks; generated programs are never executed."""
import argparse
import json
from pathlib import Path
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--fixtures", type=Path, required=True,
                    help="Destination inside the Cleave fixtures directory")
parser.add_argument("--report", type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = {
    "aead-port.py": '''from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def replace_one(path, key):
    data = path.read_bytes()
    cipher = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, data, None)
    path.write_bytes(nonce + ciphertext)
    os.rename(path, path.with_name(path.name + ".sealed"))

def sweep(key):
    for root, dirs, files in os.walk(Path.home() / "Downloads"):
        for name in files:
            if not name.endswith(".sealed"):
                replace_one(Path(root) / name, key)
''',
    "encrypted-copy.py": '''from cryptography.hazmat.primitives.ciphers.aead import AESGCM
def backup(path, key, nonce):
    ciphertext = AESGCM(key).encrypt(nonce, path.read_bytes(), None)
    path.with_suffix(".backup").write_bytes(ciphertext)
''',
    "aead-copy.rs": '''use aes_gcm::{Aes256Gcm, aead::Aead};
use std::{fs::File, io::Write, path::Path};
fn backup(cipher: &Aes256Gcm, nonce: &[u8], input: &[u8], output: &Path) {
    let encoded = cipher.encrypt(nonce.into(), input).unwrap();
    let mut file = File::create(output).unwrap();
    file.write_all(&encoded).unwrap();
}
''',
    "aead-decrypt.rs": '''use aes_gcm::{Aes256Gcm, aead::Aead};
use std::{fs::{OpenOptions, rename}, io::Write};
fn restore(cipher: &Aes256Gcm, nonce: &[u8], input: &[u8], path: &str) {
    let decoded = cipher.decrypt(nonce.into(), input).unwrap();
    let mut output = OpenOptions::new().write(true).truncate(true).open(path).unwrap();
    output.write_all(&decoded).unwrap();
    rename(path, "restored").unwrap();
}
''',
    "commented-sequence.rs": '''use aes_gcm::Aes256Gcm;
fn help(_: &Aes256Gcm) {
    // let ciphertext = cipher.encrypt(nonce, data);
    // OpenOptions::new().truncate(true).open(path);
    // file.write_all(&ciphertext);
    // rename(path, dest);
}
''',
    "source-embedding.rs": '''const SOURCE: &str = include_str!("main.rs");
fn main() { println!("{}", SOURCE); }
''',
    "commented-morph.rs": '''fn main() {
    let source = include_str!("main.rs");
    // mimicore::morph(&source, &manifest, &build, 15, name);
    println!("{}", source);
}
''',
    "generic-reader.rs": '''fn load<R: std::io::Read>(reader: &mut R) {
    let mut bytes = Vec::new();
    reader.read_to_end(&mut bytes).unwrap();
}
''',
    "prose-only.rs": '''fn main() {
    println!("Your system has been encrypted! Some program encrypted your files.");
}
''',
}
args.fixtures.mkdir(parents=True, exist_ok=True)
for name, content in fixtures.items():
    (args.fixtures / name).write_text(content)
result = subprocess.run([args.cleave, "--traits-dir", str(root), "--json",
                         str(args.fixtures)], capture_output=True, text=True,
                        check=False)
if result.returncode:
    raise SystemExit(result.stderr)
args.report.write_text(result.stdout)
files = {Path(f["path"]).name: f
         for line in result.stdout.splitlines()
         for f in json.loads(line)["files"]}
impact = "micro-behaviors/fs/write/encrypted::aead-overwrite-rename-profile"
morph = ("objectives/anti-static/obfuscation/payload/polymorphic/generator"
         "::embedded-rust-source-mutation")
for name in fixtures:
    ids = {t["id"] for t in files[name]["traits"]}
    assert (impact in ids) == (name == "aead-port.py"), (name, ids)
    assert morph not in ids, (name, ids)
    if name == "generic-reader.rs":
        assert "micro-behaviors/data/buffer/transfer::rust-reader-read-to-end" in ids
        assert not any(i.startswith("micro-behaviors/communications/http/") for i in ids)
    print("PASS", name)
