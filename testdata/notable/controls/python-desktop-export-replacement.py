import os
import shutil

user_desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
possible_dirs = [user_desktop]
for directory in set(possible_dirs):
    if not os.path.exists(directory):
        continue
    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):
            found_file = os.path.join(directory, filename)
            break

if os.path.exists(output_path):
    os.remove(output_path)
shutil.move(found_file, output_path)
