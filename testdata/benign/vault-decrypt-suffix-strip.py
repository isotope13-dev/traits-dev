"""File-vault helper: derives the output path by stripping the `.encrypted`
suffix. Removing the suffix is the unlock direction -- the result carries no
encrypted suffix, so this is not a rename *to* an encrypted target."""

import os


def unlocked_output_path(encrypted_file, output=None):
    if not output:
        output = encrypted_file.replace('.encrypted', '')
        if output == encrypted_file:
            output = encrypted_file + '.decrypted'
    return output


def rotate_name(path):
    base, _ = os.path.splitext(path)
    return base + '.rotated'
