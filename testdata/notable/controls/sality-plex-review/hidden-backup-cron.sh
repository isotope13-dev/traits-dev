#!/bin/sh
cat > "$W/.backup.sh" <<EOF
#!/bin/sh
cp "$HOME/notes" "$HOME/notes.backup"
EOF
(crontab -l; echo "* * * * * /bin/sh \"$W/.backup.sh\"") | crontab -
