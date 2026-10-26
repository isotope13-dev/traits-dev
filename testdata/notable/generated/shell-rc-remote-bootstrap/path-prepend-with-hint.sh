# Benign PATH-prepend installer with a reinstall hint elsewhere.
# The RC line persists a local PATH export, not remote execution, so neither
# the tying atom nor the hostile composite may fire here.
persist_shell_path_prepend() {
    local path_line="export PATH=\"/opt/example/bin:\$PATH\""
    printf '%s\n' "$path_line" >> "$HOME/.bashrc"
}

show_npm_alternative() {
    echo "Switch to npm: curl -fsSL https://example.com/install.sh | bash"
}
