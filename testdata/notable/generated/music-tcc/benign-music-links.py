import os
policy = '/Library/Application Support/com.apple.TCC'
print(policy)
os.symlink('/Volumes/Music', '/Users/example/Music/Music/Media.localized/Album')
os.symlink('/Volumes/State', '/Users/example/Library/Saved Application State/com.apple.Music.savedState')
