curl -fsSL "$url" -o "$target" || python3 -c 'print("retry with alternate downloader")'
