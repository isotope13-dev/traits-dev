from pathlib import Path

def transfer(sender, other):
    contents = [p.read_bytes() for p in Path("/tmp").glob("*.txt")]
    files = sender.RegisterVirtualFiles(other, None)
    return contents, files
